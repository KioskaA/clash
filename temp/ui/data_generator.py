import random
import time
import string
from datetime import date, timedelta

class DataGenerator:
    def __init__(self):
        self.cw_list = self.cw_list_generator()

    def printfromDict(self, Dict, name="Dict", showname=True):
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

    def printfromList(self, List, name="List", showname=True):
        if List == None:
            return
        if showname:
            print(f"\n--- {name} ---")
            i = 1
            for item in List:
                print(f"--- {i} ---")
                self.printfromDict(item, showname=False)
                i += 1
            print("---" + "-" * len(name) + "---")
        else:
            i = 1
            for item in List:
                print(f"--------")
                self.printfromDict(item, showname=False)
                i += 1

    def sleep(self, ms, text=False):
        if text:
            print(f"Засыпаем на {ms} миллисекунд")
            time.sleep(ms/1000)
            print(f"Проснулись")
        else:
            time.sleep(ms/1000)

    def create_members_table_data(self, size=10):
        members_table_data = []
        for _ in range(size):
            members_table_data.append({
                "tag": self.tag_generator(),
                "name": self.name_generator(),
                "activity_points": random.randint(0, 100)
            })
        self.members_table_data = members_table_data
        return members_table_data

    def tag_generator(self):
        tag_length = random.randint(9, 10)
        chars_after_hash = tag_length - 1
        allowed_chars = string.ascii_uppercase + string.digits
        random_chars = ''.join(random.choices(allowed_chars, k=chars_after_hash))
        return f"#{random_chars}"

    def name_generator(self):
        first_names = [
            "Alexander", "Benjamin", "Christopher", "Daniel", "Edward",
            "Frederick", "George", "Henry", "Isaac", "James",
            "Kevin", "Leonard", "Michael", "Nicholas", "Oliver",
            "Patrick", "Quentin", "Richard", "Samuel", "Thomas",
            "Victoria", "Anna", "Maria", "Elizabeth", "Sarah",
            "Jennifer", "Jessica", "Amanda", "Ashley", "Emma",
            "Olivia", "Sophia", "Isabella", "Mia", "Charlotte",
            "Amelia", "Harper", "Evelyn", "Abigail", "Emily"
        ]
        name = random.choice(first_names)
        return name
    
    def create_player_frame_data(self):
        player_frame_data = []
        for member in self.members_table_data:
            cwl_participation = random.choice([True, False])
            cwl_attacks = random.randint(0, 7) if cwl_participation else 0
            cwl_stars = cwl_attacks*random.randint(0, 3) if cwl_participation else 0

            cw_participations = random.randint(0, 10)
            cw_with_attacks = random.randint(0, cw_participations)
            cw_no_attacks = cw_participations - cw_with_attacks

            raid_participations = random.randint(0, 4)
            raid_available_attacks = 4*random.randint(5, 6)
            raid_attacks = raid_participations*random.randint(0, 6)
            while raid_attacks > raid_available_attacks:
                raid_attacks -= 1
            
            player_frame_data.append({
                "tag": member["tag"],
                "name": member["name"],
                "level": random.randint(20, 150),
                "th_level": random.randint(7, 12),
                "cg_points": random.randint(0, 1000),
                "CCcontributions": f"{random.randint(0, 1500)}/{random.randint(0, 1500)}",
                "buildings_upgraded": random.randint(2, 15),
                "days_offline": random.randint(0, 5),
                "capital_contibutions": random.randint(5000, 50000),
                "cwl": {"participation": cwl_participation, "attacks": cwl_attacks, "stars": cwl_stars},
                "cw": {"participation": cw_participations, "no_attacks": cw_no_attacks, "with_attacks":cw_with_attacks},
                "raids": {"participation": raid_participations, "attacks": raid_attacks, "available_attacks": raid_available_attacks}
            })
        self.player_frame_data = player_frame_data
        return player_frame_data
    
    def create_extra_panel_data(self):
        extra_panel_data = []
        i = 0
        for member in self.members_table_data:
            extra_panel_data.append({
                "tag": member["tag"],
                "cwl": {},
                "cw": self.cw_member_data_generator(),
                "raids": {}
            })
            i += 1
        data = self.sort_cw_by_date(extra_panel_data, True)
        self.extra_panel_data = data
        return data
    
    def sort_cw_by_date(self, data, reverse=True):
        for member in data:
            if "cw" in member and member["cw"]:
                member["cw"].sort(key=lambda x: x.get("date", ""), reverse=reverse)
        return data
    
    def cw_member_data_generator(self):
        cw_member_data = []
        for cw_id in range(len(self.cw_list)):
            cw_member_data.append({
                "id": self.cw_list[cw_id]["id"],
                "date": self.cw_list[cw_id]["date"],
                "result": self.cw_list[cw_id]["result"],
                "participation": random.choice([True, False]),
                "attacks": random.randint(0, 2),
                "stars": random.randint(0, 3)
            })
        return cw_member_data

    def cw_list_generator(self, amount=5):
        cw_list = []
        Date = date(2026, 1, 29)
        for i in range(1, amount+1):
            cw_list.append({
                "id": i,
                "date": str(Date + timedelta(2*i)),
                "result": random.choice(["win", "lose", "tie"])
            })
        return cw_list


if __name__ == "__main__":
    dg = DataGenerator()
    members_table_data = dg.create_members_table_data(2)
    player_frame_data = dg.create_player_frame_data()
    extra_panel_data = dg.create_extra_panel_data()
    cw_list = dg.cw_list_generator()
    tempdata = dg.cw_member_data_generator()
    dg.printfromList(tempdata, name="Игроки", showname=False)