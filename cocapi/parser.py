import os
import json
import datetime

class Parser():
    def __init__(self):
        self.client = None
        self._logged_in = None
        os.makedirs("saves", exist_ok=True)
        os.makedirs("saves/clan_wars", exist_ok=True)
        print("FullData.__init__: success")
        
    async def get_cw(self, clantag, save=False): # coc.get_current_war(tag) → ClanWar | None
        cw = await self.client.get_current_war(clantag)
        if cw.is_cwl:
            return None
        
        path = os.path.join("saves", "clan_wars")

        data = {
            "id": self.find_available_id(path),
            "savetime": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "opponent": (cw.opponent.tag, cw.opponent.name),
            "end": str(cw.end_time.time.date()),
            "team_size": int(cw.team_size),
            "status": str(cw.status),
            "members": self.parse_cw_members(cw.clan.members)
        }
        if save:
            filename = f"war_{cw.end_time.time.date().strftime('%d_%m_%Y')}.json"
            filepath = os.path.join(path, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"Данные войны сохранены в файл: {filepath}")
        return data
    
    def parse_cw_members(self, members):
        data = []
        for member in members:
            data.append({
                "tag": member.tag,
                "name": member.name,
                "attacks_count": len(member.attacks),
                "stars": member.star_count
            })
        return data
    
    def find_available_id(self, path):
        max_id = 1
        for file in os.listdir(path):
            if file.endswith('.json'):
                with open(os.path.join(path, file), 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    current_id = data.get('id', 1)
                    if current_id > max_id:
                        max_id = current_id
        return max_id+1


def printfromDict(Dict, name="Dict", showname = True):
    if Dict == None:
        return
    if showname:
        print(f"\n--- {name} ---")
        for key, value in Dict.items():
            print(f"{key}: {value}")
        print("---" + "-" * len(name) + "---")
    elif not showname:
        for key, value in Dict.items():
            print(f"{key}: {value}")


async def main():
    getter = None
    try:
        getter = FullData()
        await getter.login(APILogin, APIPassword)

        cw = await getter.get_cw(Clantag, save=False)
        printfromDict(cw, "CW")

        print("Тестовый запуск успешен")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        if getter:
            await getter.logout()

if __name__=="__main__":
    asyncio.run(main())