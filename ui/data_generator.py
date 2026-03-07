import random
import time
import string
from datetime import date, timedelta

class DataGenerator:
    def __init__(self):
        self.members_table_data = None
        self.player_frame_data = None
        self.extra_panel_data = None
        self.cw_list = None          # общий список войн
        self.raids_list = None        # общий список рейдов
        self.cwl_list = None          # общий список ЛВК (обычно один)
        self.clan_size = None

    # ---------- публичные методы (вызываются из ui.py) ----------
    def create_members_table_data(self, size=10):
        if self.members_table_data is None:
            self._generate_all_data(size)
        return self.members_table_data

    def create_player_frame_data(self):
        if self.player_frame_data is None:
            # если ещё нет данных, генерируем с размером из members_table_data или 10
            if self.members_table_data is not None:
                self._generate_all_data(len(self.members_table_data))
            else:
                self._generate_all_data(10)
        return self.player_frame_data

    def create_extra_panel_data(self):
        if self.extra_panel_data is None:
            if self.members_table_data is not None:
                self._generate_all_data(len(self.members_table_data))
            else:
                self._generate_all_data(10)
        return self.extra_panel_data

    # ---------- внутренняя генерация всего набора данных ----------
    def _generate_all_data(self, size):
        # 1. члены клана
        self.members_table_data = self._generate_members(size)

        # 2. общие списки событий
        self.cw_list = self._generate_cw_list(amount=5)
        self.raids_list = self._generate_raids_list(amount=4)
        self.cwl_list = self._generate_cwl_list()  # например, одна ЛВК

        # 3. детальные данные для extra_panel
        self.extra_panel_data = []
        for member in self.members_table_data:
            tag = member["tag"]
            extra = {
                "tag": tag,
                "raids": self._generate_member_raids(tag),
                "cw": self._generate_member_cw(tag),
                "cwl": self._generate_member_cwl(tag)
            }
            self.extra_panel_data.append(extra)

        # 4. сводные данные для player_frame на основе детальных
        self.player_frame_data = []
        for i, member in enumerate(self.members_table_data):
            extra = self.extra_panel_data[i]   # соответствие по индексу
            base = self._generate_player_base(member)
            base["cwl"] = self._summarize_cwl(extra["cwl"])
            base["cw"] = self._summarize_cw(extra["cw"])
            base["raids"] = self._summarize_raids(extra["raids"])
            self.player_frame_data.append(base)

        # 5. сортировка детальных данных по датам (как в оригинале)
        self.extra_panel_data = self.sort_cw_by_date(self.extra_panel_data, True)

    # ---------- генерация базовых сущностей ----------
    def _generate_members(self, size):
        members = []
        for _ in range(size):
            members.append({
                "tag": self.tag_generator(),
                "name": self.name_generator(),
                "activity_points": random.randint(0, 100)
            })
        return members

    def _generate_cw_list(self, amount=5):
        cw_list = []
        start_date = date(2026, 1, 29)
        for i in range(1, amount + 1):
            cw_list.append({
                "id": i,
                "date": str(start_date + timedelta(days=2 * i)),
                "result": random.choice(["win", "lose", "tie"])
            })
        return cw_list

    def _generate_raids_list(self, amount=4):
        raids_list = []
        start_date = date(2026, 1, 29)
        for i in range(1, amount + 1):
            raids_list.append({
                "id": i,
                "date": str(start_date + timedelta(weeks=i))
            })
        return raids_list

    def _generate_cwl_list(self):
        # можно расширить до нескольких ЛВК, пока одна
        return [{"id": 1, "date": "2026-03"}]

    # ---------- генерация данных для конкретного игрока (extra) ----------
    def _generate_member_raids(self, tag):
        member_raids = []
        for raid in self.raids_list:
            # с вероятностью 80% игрок участвует
            if random.random() < 0.8:
                attacks = random.randint(1, 6)
                gold = attacks * random.randint(500, 2000)
            else:
                attacks = 0
                gold = 0
            member_raids.append({
                "id": raid["id"],
                "state": "ended",
                "date": raid["date"],
                "attacks": attacks,
                "available_attacks": 6,
                "gold_earned": gold
            })
        return member_raids

    def _generate_member_cw(self, tag):
        member_cw = []
        for cw in self.cw_list:
            participation = random.random() < 0.7   # участвует в 70% войн
            if participation:
                # теперь атаки могут быть 0, 1 или 2
                attacks = random.randint(0, 2)
                stars = random.randint(0, 3) if attacks else 0
            else:
                attacks = 0
                stars = 0
            member_cw.append({
                "id": cw["id"],
                "date": cw["date"],
                "result": cw["result"],
                "participation": participation,
                "attacks": attacks,
                "stars": stars
            })
        return member_cw

    def _generate_member_cwl(self, tag):
        # 50% игроков не участвуют в ЛВК
        if random.random() < 0.5:
            return {}
        # участвует – генерируем дни
        days = []
        for day in range(1, 8):
            replaced = random.random() < 0.1
            if replaced:
                attack = False
                stars = 0
                percentage = 0
            else:
                attack = random.random() < 0.8
                if attack:
                    # теперь звезды могут быть 0,1,2,3 с разными весами (настройте по желанию)
                    stars = random.choices([0,1,2,3], weights=[0.1, 0.3, 0.3, 0.3])[0]
                    if stars == 0:
                        percentage = random.randint(0, 49)      # 0 звёзд – меньше 50%
                    elif stars == 1:
                        percentage = random.randint(4, 92)
                    elif stars == 2:
                        percentage = random.randint(50, 99)
                    else:  # stars == 3
                        percentage = 100
                else:
                    stars = 0
                    percentage = 0
            days.append({
                "day": day,
                "replaced": replaced,
                "attack": attack,
                "stars": stars,
                "percentage": percentage
            })
        return {
            "id": 1,
            "date": "2026-03",
            "days": days
        }

    # ---------- базовая информация для player_frame (не зависящая от активностей) ----------
    def _generate_player_base(self, member):
        return {
            "tag": member["tag"],
            "name": member["name"],
            "level": random.randint(20, 150),
            "th_level": random.randint(7, 12),
            "cg_points": random.randint(0, 10000),
            "CCcontributions": f"{random.randint(0, 1500)}/{random.randint(0, 1500)}",
            "buildings_upgraded": random.randint(2, 15),
            "days_offline": random.randint(0, 5),
            "capital_contibutions": random.randint(5000, 50000)
        }

    # ---------- сводки из детальных данных ----------
    def _summarize_cwl(self, cwl_data):
        if not cwl_data:
            return {"participation": False, "attacks": 0, "stars": 0}
        days = cwl_data["days"]
        attacks = sum(1 for d in days if d["attack"])
        stars = sum(d["stars"] for d in days if d["attack"])
        return {
            "participation": attacks > 0,
            "attacks": attacks,
            "stars": stars
        }

    def _summarize_cw(self, cw_list):
        participations = sum(1 for cw in cw_list if cw["participation"])
        with_attacks = sum(1 for cw in cw_list if cw["attacks"] > 0)
        no_attacks = participations - with_attacks
        return {
            "participation": participations,
            "with_attacks": with_attacks,
            "no_attacks": no_attacks
        }

    def _summarize_raids(self, raids_list):
        participations = sum(1 for r in raids_list if r["attacks"] > 0)
        total_attacks = sum(r["attacks"] for r in raids_list)
        total_available = sum(r["available_attacks"] for r in raids_list)
        return {
            "participation": participations,
            "attacks": total_attacks,
            "available_attacks": total_available
        }

    # ---------- вспомогательные методы (оставлены без изменений) ----------
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
        return random.choice(first_names)

    def printfromDict(self, Dict, name="Dict", showname=True):
        if Dict is None:
            return
        if showname:
            print(f"\n--- {name} ---")
            for key, value in Dict.items():
                print(f"{key}: {value}")
            print("---" + "-" * len(name) + "---")
        else:
            for key, value in Dict.items():
                print(f"{key}: {value}")

    def printfromList(self, List, name="List", showname=True):
        if List is None:
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
            time.sleep(ms / 1000)
            print(f"Проснулись")
        else:
            time.sleep(ms / 1000)

    def sort_cw_by_date(self, data, reverse=True):
        for member in data:
            if "cw" in member and member["cw"]:
                member["cw"].sort(key=lambda x: x.get("date", ""), reverse=reverse)
            if "raids" in member and member["raids"]:
                member["raids"].sort(key=lambda x: x.get("date", ""), reverse=reverse)
        return data


if __name__ == "__main__":
    dg = DataGenerator()
    dg.create_members_table_data(5)
    dg.create_player_frame_data()
    dg.create_extra_panel_data()
    dg.printfromList(dg.members_table_data, name="Участники")
    dg.printfromList(dg.player_frame_data, name="Карточки игроков")
    dg.printfromList(dg.extra_panel_data, name="Детальные данные")