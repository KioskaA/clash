import random
import time
import string

class DataGenerator:
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


if __name__ == "__main__":
    dg = DataGenerator()
    members_table_data = dg.create_members_table_data(2)
    player_frame_data = dg.create_player_frame_data()
    dg.printfromList(player_frame_data, name="Игроки", showname=True)