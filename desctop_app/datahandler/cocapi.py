import coc
import asyncio
from desctop_app.config import settings

APILogin = settings.coc_api["login"]
APIPassword = settings.coc_api["password"]
Clantag = settings.coc_api["clantag"]

class DataGetter():
    def __init__(self):
        self.client = None
        self.clan = None
        self._logged_in = False

    async def login(self, email, password):
        try:
            self.client = coc.Client(cache_max_size=0)
            await self.client.login(email, password)
            self._logged_in = True
            print(f"DataGetter.login(): success")
        except Exception as e:
            print(f"DataGetter.login(): error - {e}")
            raise

    async def logout(self):
        if self.client and self._logged_in:
            try:
                await self.client.close()
                self._logged_in = False
                print(f"DataGetter.logout(): logout")
            except Exception as e:
                print(f"DataGetter.logout(): error - {e}")

    async def get_raids_data(self, clantag):
        logs = await self.client.get_raid_log(clantag, limit=1)
        logs = list(logs)
        raidlog = []
        for log in logs:
            raidlog.append({
                "state": log.state,
                "end_time": str(log.end_time.time),
                "attack_count": log.attack_count,
                "offensive_reward": log.offensive_reward,
                "defensive_reward": log.defensive_reward,
                "total_loot": log.total_loot,
                "completed_raid_count": log.completed_raid_count,
                "members": self.parse_raid_members(log.members)
            })
        return raidlog[0]
    
    def check_is_player_attacked_in_raids(self, playertag, raidlog) -> True | False:
        for member in raidlog["members"]:
            member_tag = member["tag"]
            if member_tag == playertag:
                return True
        return False
    
    def finalize_raidweekend(self, players, raidlog) -> dict:
        raid = raidlog
        checked_members = self.check_all_members_for_attacks_in_raidweekend(players, raidlog)
        raid.update({
            "overlooked_members": checked_members[0],
            "attacked_members": checked_members[1]
        })
        return raid
    
    def check_all_members_for_attacks_in_raidweekend(self, players, raidlog):
        tags = []
        for player in players:
            tags.append(player["tag"])
        overlooked_members = []
        attacked_members = []
        for tag in tags:
            if not self.check_is_player_attacked_in_raids(tag, raidlog):
                overlooked_members.append(tag)
            else:
                attacked_members.append(tag)
        return overlooked_members, attacked_members
    
    async def get_players_data(self, clantag):
        clan = await self.client.get_clan(clantag)
        players = []
        async for player in clan.get_detailed_members():
            players.append({
                "tag": player.tag,
                "name": player.name,
                "role": player.role.in_game_name,
                "clan_capital_contributions": player.clan_capital_contributions,
                "exp_level": player.exp_level,
                "builder_base_league": player.builder_base_league.name,
                "trophies": player.trophies,
                "builder_base_trophies": player.builder_base_trophies,
                "town_hall": player.town_hall,
                "donations": player.donations,
                "received": player.received,
                "builder_hall": player.builder_hall,
                "war_opted_in": player.war_opted_in,
                "achievements": self.parse_achievement(player.achievements),
                "builder_troops": self.parse_troops(player.builder_troops),
                "equipment": self.parse_troops(player.equipment),
                "heroes": self.parse_troops(player.heroes),
                "home_troops": self.parse_troops(player.home_troops),
                "pets": self.parse_troops(player.pets),
                "spells": self.parse_troops(player.spells),
            })
        return players
    
    def parse_achievement(self, achievements):
        result = []
        for achievement in achievements:
            result.append({
                "name": achievement.name,
                "stars": achievement.stars,
                "value": achievement.value,
                "target": achievement.target
            })
        return result

    def parse_troops(self, troops):
        result = []
        for troop in troops:
            result.append({
                "name": troop.name,
                "level": troop.level,
            })
        return result
    
    def parse_raid_members(self, memberslist):
        members = []
        for member in memberslist:
            members.append({
                "tag": member.tag,
                "name": member.name,
                "attack_count": member.attack_count,
                "attack_limit": member.attack_limit,
                "bonus_attack_limit": member.bonus_attack_limit,
                "capital_resources_looted": member.capital_resources_looted
            })
        return members
    
    async def get_cwl(self, clantag):
        war = await self.client.get_current_war(clantag)
        if not war.is_cwl:
            return "GOT CW INSTEAD OF CWL"
        cwl = await self.parse_league_group(war.league_group, clantag, war.team_size)
        return cwl
    
    async def parse_league_group(self, league_group, clantag, team_size):
        clans = league_group.clans
        for clan in clans:
            if clan.tag == clantag:
                home_clan = clan
                break
        home_clan = self.parse_league_clan(home_clan)
        clans = self.parse_league_clans(clans)
        wars = []
        async for war in league_group.get_wars_for_clan(clantag):
            wars.append(self.parse_league_war(war))
        group = {
            "team_size": team_size,
            "state": league_group.state,
            "season": league_group.season,
            "number_of_rounds": league_group.number_of_rounds,
            "clans": clans,
            "home_clan": home_clan,
            "home_clan_wars": wars,
            "overlooked_players": self.get_overlooked_players(wars, [m["tag"] for m in home_clan["members"]])
        }
        return group
    
    def get_overlooked_players(self, wars, members):
        completed_wars = [war for war in wars if war.get('state') == 'War Ended']
        num_rounds = len(completed_wars)

        if num_rounds == 0:
            return {}

        result = {i: [] for i in range(1, num_rounds + 1)}

        for player in members:
            missed = 0
            for war in completed_wars:
                attacked = war.get('attacked_players', [])
                if player not in attacked:
                    missed += 1

            if 1 <= missed <= num_rounds:
                result[missed].append(player)

        return result
    
    def parse_league_war(self, war):
        attacks = self.parse_league_attacks(war.attacks, war.clan.members)
        league_war = {
            "opponent": (war.opponent.tag, war.opponent.name),
            "state": str(war.state),
            "end_time": str(war.end_time.time),
            "war_tag": war.war_tag,
            "attacks": attacks,
            "status": war.status,
            "attacked_players": self.league_attacker_tags(attacks)
        }
        return league_war

    def league_attacker_tags(self, attacks):
        tags = []
        for attack in attacks:
            tags.append(attack["attacker_tag"])
        return tags

    def check_is_home_league_attack(self, attack, members):
        attacker_tag = attack.attacker_tag
        members = self.parse_league_members(members)
        attacker_tags = []
        for member in members:
            attacker_tags.append(member["tag"])
        if attacker_tag in attacker_tags:
            return True
        else:
            return False

    def parse_league_attacks(self, attacks, war):
        league_attacks = []
        for attack in attacks:
            if self.check_is_home_league_attack(attack, war):
                league_attacks.append(self.parse_league_attack(attack))
        return league_attacks

    def parse_league_attack(self, attack):
        league_attack = {
            "stars": attack.stars,
            "destruction": attack.destruction,
            "attacker_tag": attack.attacker_tag,
            "defender_tag": attack.defender_tag,
            "duration": attack.duration
        }
        return league_attack
    
    def parse_league_clan(self, clan):
        league_clan = {
            "tag": clan.tag,
            "name": clan.name,
            "members": self.parse_league_members(clan.members)
        }
        return league_clan
    
    def parse_league_clans(self, clans):
        league_clans = []
        for clan in clans:
            league_clans.append(self.parse_league_clan(clan))
        return league_clans
    
    def parse_league_members(self, members):
        league_members = []
        for member in members:
            league_members.append({
                "tag": member.tag,
                "name": member.name,
                "town_hall": member.town_hall
            })
        return league_members
    
    async def get_cw(self, clantag):
        war = await self.client.get_current_war(clantag)
        if war == None:
            return "NO WAR"
        if war.is_cwl:
            return "GOT CWL INSTEAD OF CW"
        home_members = self.parse_home_members(war.clan, war.members)
        home_attacks = self.verify_attacks(home_members, war.attacks)
        attack_states = self.create_cw_attackers_list(home_members)
        cw = {
            "home_clan": war.clan,
            "opponent": war.opponent,
            "state": str(war.state),
            "end_time": str(war.end_time.time),
            "team_size": war.team_size,
            "status": str(war.status),
            "home_members": home_members,
            "attacks": home_attacks,
            "ovelooked_members": attack_states[0],
            "attacked_members": attack_states[1]
        }
        return cw
    
    def parse_cw_attacks(self, attacks):
        cw_attacks = []
        for attack in attacks:
            cw_attacks.append({
                "stars": attack.stars,
                "destruction": attack.destruction,
                "attacker_tag": attack.attacker_tag,
                "duration": attack.duration,
            })
        return cw_attacks

    def check_for_cw_attack(self, member):
        if isinstance(member["attacks"], list) and len(member["attacks"]) > 0:
            return True, member["tag"]
        else:
            return False, member["tag"]
    
    def create_cw_attackers_list(self, members):
        ovelooked_members = []
        attacked_members = []
        for member in members:
            res = self.check_for_cw_attack(member)
            if res[0] == True:
                attacked_members.append(res[1])
            else:
                ovelooked_members.append(res[1])
        return ovelooked_members, attacked_members
    
    def verify_members(self, clan, members):
        home_members = []
        for member in members:
            if member.clan == clan:
                home_members.append(member)
        return home_members
    
    def verify_attacks(self, home_members, attacks):
        home_members_tags = []
        for member in home_members:
            home_members_tags.append(member["tag"])
        home_attacks = []
        for attack in attacks:
            if attack.attacker_tag in home_members_tags:
                home_attacks.append(attack)
        return self.parse_cw_attacks(home_attacks)

    def parse_home_members(self, clan, members):
        home_members = []
        for member in self.verify_members(clan, members):
            home_members.append({
                "tag": member.tag,
                "name": member.name,
                "town_hall": member.town_hall,
                "star_count": member.star_count,
                "attacks": self.parse_cw_attacks(member.attacks)
            })
        return home_members


    async def verify_(self, playertag, token):
        t = await self.client.verify_player_token(playertag, token)
        return t


def process_nested_data(data, depth=2, output_type='print', filename=None, encoding='utf-8'):
    """
    Обрабатывает вложенные структуры данных с заданными параметрами.
    
    Args:
        data: данные для обработки (словарь, список или другой тип)
        depth: максимальная глубина вывода (по умолчанию 2)
        output_type: тип вывода ('print' - только печать, 'string' - сохранение в файл)
        filename: имя файла для сохранения (обязателен при output_type='string')
        encoding: кодировка файла (по умолчанию utf-8)
    
    Returns:
        str: отформатированная строка при output_type='string', иначе None
    
    Raises:
        ValueError: если указан неправильный тип вывода или отсутствует filename
    """
    # Проверка параметров
    if output_type not in ['print', 'string']:
        raise ValueError("output_type должен быть 'print' или 'string'")
    
    if output_type == 'string' and filename is None:
        raise ValueError("При output_type='string' необходимо указать filename")
    
    # Внутренняя рекурсивная функция для форматирования
    def _format_data(data, current_depth=0, indent=0, is_list_item=False):
        result = ""
        prefix = "  " * indent
        if is_list_item:
            prefix += "- "
        
        # Если достигли максимальной глубины
        if current_depth >= depth:
            if isinstance(data, dict):
                result += f"{prefix}{{...}} (словарь с {len(data)} элементами)\n"
            elif isinstance(data, list):
                result += f"{prefix}[...] (список из {len(data)} элементов)\n"
            else:
                result += f"{prefix}{data}\n"
            return result
        
        # Обработка словаря
        if isinstance(data, dict):
            for key, value in data.items():
                result += f"{prefix}{key}: "
                if isinstance(value, (dict, list)):
                    result += "\n" + _format_data(value, current_depth + 1, indent + 1)
                else:
                    result += f"{value}\n"
        
        # Обработка списка
        elif isinstance(data, list):
            for i, item in enumerate(data):
                if isinstance(item, (dict, list)):
                    result += f"{prefix}Элемент {i + 1}:\n"
                    result += _format_data(item, current_depth + 1, indent + 1, True)
                else:
                    result += f"{prefix}- {item}\n"
        
        # Обработка простых типов
        else:
            result += f"{prefix}{data}\n"
        
        return result
    
    # Форматируем данные
    formatted_string = _format_data(data)
    
    # Обработка в зависимости от типа вывода
    if output_type == 'print':
        print(formatted_string, end='')
        return None
    else:  # output_type == 'string'
        try:
            with open(filename, 'w', encoding=encoding) as f:
                f.write(formatted_string)
            print(f"Данные успешно сохранены в файл: {filename}")
            return formatted_string
        except Exception as e:
            print(f"Ошибка при сохранении файла: {e}")
            return None

async def main():
    getter = None
    try:
        getter = DataGetter()
        await getter.login(APILogin, APIPassword)


        players = await getter.get_players_data(Clantag)
        process_nested_data(players, depth=20, output_type="string", filename="players")

        raidlog = await getter.get_raids_data(Clantag)
        raid = getter.finalize_raidweekend(players, raidlog)
        process_nested_data(raid, depth=20, output_type="string", filename="raid")

        cwl = await getter.get_cwl(Clantag)
        process_nested_data(cwl, depth=20, output_type="string", filename="cwl")

        cw = await getter.get_cw("#2R8CP9G98")
        process_nested_data(cw, depth=20, output_type="string", filename="cw")

        #t = await getter.verify_("#YGGRO2YV2", "xddhhp3a") # Для проверки является ли пользователь главой клана
        #print(t)


        print("Тестовый запуск успешен")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        if getter:
            await getter.logout()

if __name__ == "__main__":
    asyncio.run(main())