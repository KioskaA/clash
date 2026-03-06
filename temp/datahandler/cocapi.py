import coc
import asyncio
from config import settings

APILogin = settings.coc_api["login"]
APIPassword = settings.coc_api["password"]
Clantag = settings.coc_api["clantag"]

Wartag = None
Playertag = "#R2CLJL8YR"
Playertags = None
AuthToken = None

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
                "completed_raid_count": log.total_loot,
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
                "received": player.received
            })
        return players
    
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
        cwl = {
            #"clan": war.clan,
            #"opponent": war.opponent,
            #"state": war.state.in_game_name,
            #"end_time": str(war.end_time.time),
            #"team_size": war.team_size,
            "league_group": await self.parse_league_group(war.league_group, clantag),
            #"attacks": war.attacks,
            #"members": war.members,
        }
        return cwl
    
    async def parse_league_group(self, league_group, clantag):
        wars = []
        async for war in league_group.get_wars_for_clan(clantag):
            wars.append(war)
        group = {
            "season": league_group.season,
            "number_of_rounds": league_group.number_of_rounds,
            "clans": league_group.clans,
            "home_clan_wars": wars
        }
        return group

    async def getdata(self):
        await self.client.get_clan(Clantag)
        await self.client.get_clan_war(Clantag)
        await self.client.get_league_group(Clantag)
        await self.client.get_members(Clantag)
        await self.client.get_player(Playertag)
        await self.client.verify_player_token(Playertag, AuthToken)


async def main():
    getter = None
    try:
        getter = DataGetter()
        await getter.login(APILogin, APIPassword)

        #print(f"raids start: {coc.utils.get_raid_weekend_start()}")
        #print(f"raids end: {coc.utils.get_raid_weekend_end()}")
        #raidlog = await getter.get_raids_data(Clantag)
        #print(raidlog)
        #print(getter.check_is_player_attacked_in_raids(Playertag, raidlog))
        #players = await getter.get_players_data(Clantag)
        #print(getter.finalize_raidweekend(players, raidlog))

        cwl = await getter.get_cwl(Clantag)
        print(cwl)



        print("Тестовый запуск успешен")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        if getter:
            await getter.logout()

if __name__ == "__main__":
    asyncio.run(main())