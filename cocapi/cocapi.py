import coc
import asyncio
from config import settings

APILogin = settings.coc_api["login"]
APIPassword = settings.coc_api["password"]
Clantag = settings.coc_api["clantag"]

playertags = ["#R2CLJL8YR", "#YGGR02YV2", "#Y2RR2Q2JC", "#GJPCU8Q92", "#GUYP8QUPY"]

class DataGetter():
    def __init__(self):
        self.client = None
        self.clan = None
        self._logged_in = False
        self.members = []
        print(f"DataGetter.__init__(): success")

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

    async def getClanMembers_byclantag(self, clantag):
        if not self._logged_in:
            raise Exception("Client not logged in")
        
        self.clan = await self.client.get_clan(clantag)
        players = []
        async for player in self.clan.get_detailed_members():
            players.append({
                "tag": player.tag,
                "name": player.name
            })
        return players

    async def getClanMembers(self):
        if not self._logged_in:
            raise Exception("Client not logged in")
        if self.clan is None:
            return []
            
        members = []
        try:
            async for player in self.clan.get_detailed_members():
                CCcontributions = f"{player.donations}/{player.received}"
                members.append({
                    "tag": player.tag,
                    "name": player.name,
                    "level": player.exp_level,
                    "th_level": player.town_hall,
                    "cg_value": 0,
                    "CCcontributions_value": CCcontributions,
                    "buildings_upgraded_value": 0,
                    "days_offline_value": 0,
                    "capital_contibutions_value": player.clan_capital_contributions,
                    "cwl_participation_value": 0,
                    "cwl_attacks_value": 0,
                    "cwl_stars_value": 0,
                    "cw_participation_value": 0,
                    "cw_no_attacks_value": 0,
                    "cw_with_attacks_value": 0,
                    "raid_participation_value": 0,
                    "raid_attacks_value": 0,
                    "raid_available_attacks_value": 0,
                })
                self.members = members
        except Exception as e:
            print(f"Error getting clan members: {e}")
            return []
        return members
    
    async def finalize_members(self):
        #cwl_logs = await self._get_logs(type="cwl")
        #cw_logs = await self._get_logs(type="cw")
        #self._handle_cwl_log(cwl_logs[0])
        self.raid_logs = await self._get_logs(type="raids")
        self._handle_raid_logs(self.raid_logs)

    async def _get_logs(self, type=None):
        logs = []
        if type == "cwl" or type == "cw":
            logs = await self.client.get_war_log(self.clan.tag, limit=12)
        elif type == "raids":
            logs = await self.client.get_raid_log(self.clan.tag, limit=5)

        logs = list(logs)

        if type == "cwl":
            cwl_logs = []
            for log in logs:
                if log.is_league_entry:
                    cwl_logs.append(log)
            return cwl_logs
        elif type == "cw":
            cw_logs = []
            for log in logs:
                if not log.is_league_entry:
                    cw_logs.append(log)
            return cw_logs
        elif type == "raids":
            raid_logs = []
            for log in logs:
                raid_logs.append({
                    "state": log.state,
                    "start_time": log.start_time,
                    "end_time": log.end_time,
                    "members": "YES" if len(log.members) > 0 else "EMPTY",
                })
            return raid_logs

    async def _handle_cwl_log(self, cwllog):
        if not hasattr(self, "warclan"):
            self.warclan = cwllog.clan
        
    async def _handle_raid_logs(self, raidlogs):
        pass

    async def on_member_selected(self, tag):
        try:
            if len(self.members) == 0:
                await self.getClanMembers()
                await self.finalize_members()
            for player in self.members:
                if player["tag"] == tag:
                    return player
            print(f"Игрок с тегом {tag} не найден")
            return None
        except Exception as e:
            print(f"Error in on_member_selected: {e}")
            return None


async def main():
    getter = None
    try:
        getter = DataGetter()
        await getter.login(APILogin, APIPassword)

        getter.clan = await getter.client.get_clan(Clantag)
        log = await getter._get_logs(type="raids")
        print(log)

        print("Тестовый запуск успешен")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        if getter:
            await getter.logout()

if __name__=="__main__":
    asyncio.run(main())