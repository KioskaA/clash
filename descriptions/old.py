"""def __init__(self):
        super().__init__("Информация об игроке")
        self.setFixedWidth(750)
        self.setAlignment(Qt.AlignCenter)
        
        # Создаем основной вертикальный layout для рамки
        frame_layout = QVBoxLayout(self)
        
        # Верхняя строка с двумя надписями
        top_row_layout = QHBoxLayout()
        top_row_layout.setSpacing(15)
        
        self.label_tag = QLabel("Тег")
        self.label_tag.setFont(QFont("Arial", 10, QFont.Bold))
        
        self.label_nick = QLabel("Никнейм")
        self.label_nick.setFont(QFont("Arial", 10, QFont.Bold))
        
        top_row_layout.addWidget(self.label_tag)
        top_row_layout.addWidget(self.label_nick)
        top_row_layout.addStretch()
        
        # Добавляем верхнюю строку в основной layout
        frame_layout.addLayout(top_row_layout)
        
        # Добавляем небольшой отступ
        frame_layout.addSpacing(10)
        
        # Надпись "За последние 30 дней:"
        self.label_last_30_days = QLabel("За последние 30 дней:")
        self.label_last_30_days.setFont(QFont("Arial", 9))
        frame_layout.addWidget(self.label_last_30_days)
        
        # Создаем надписи в столбик
        self.activity_labels = []

        self.activity_labels_text = [
            "Очки игр кланов: ", # 0
            "Пожертвовал войск: ", # 1
            "Получил войск: ", # 2
            "Апгрейд деревень: ", # 3
            "Дней оффлайн: ", # 4
            "Золота столицы пожертвовано: ", # 5
        ]
        cg = QLabel(f"{self.activity_labels_text[0]}")
        self.activity_labels.append(cg)
        CCcontributions = QLabel(f"{self.activity_labels_text[1]}")
        self.activity_labels.append(CCcontributions)
        buildings_upgraded = QLabel(f"{self.activity_labels_text[3]}")
        self.activity_labels.append(buildings_upgraded)
        days_offline = QLabel(f"{self.activity_labels_text[4]}")
        self.activity_labels.append(days_offline)
        capital_contibutions = QLabel(f"{self.activity_labels_text[5]}")
        self.activity_labels.append(capital_contibutions)

        for label in self.activity_labels:
            label.setFont(QFont("Arial", 8))
            frame_layout.addWidget(label)

        # Добавляем раздел "ЛВК"
        self.lwk_group = QGroupBox("ЛВК")
        lwk_layout = QHBoxLayout(self.lwk_group)
            
        self.cwl_activity_labels_text = [
            "Участие: ",
            "Атаки: ",
            "Звёзды: ",
        ]
        
        self.cwl_activity_labels = []
        cwl_participation = QLabel(f"{self.cwl_activity_labels_text[0]}")
        self.cwl_activity_labels.append(cwl_participation)
        cwl_attacks = QLabel(f"{self.cwl_activity_labels_text[1]}")
        self.cwl_activity_labels.append(cwl_attacks)
        cwl_stars = QLabel(f"{self.cwl_activity_labels_text[2]}")
        self.cwl_activity_labels.append(cwl_stars)

        for label in self.cwl_activity_labels:
            label.setFont(QFont("Arial", 8))
            lwk_layout.addWidget(label)

        # Кнопка "Подробнее" для ЛВК
        self.lwk_detail_button = QPushButton("Подробнее")
        self.lwk_detail_button.setFixedWidth(100)

        frame_layout.addWidget(self.lwk_group)
        lwk_layout.addWidget(self.lwk_detail_button)

        self.cw_activity_labels_text = [
            "Участий: ",
            "Без атак: ",
            "С атаками: ",
        ]
        self.raid_activity_labels_text = [
            "Участий: ",
            "Атаки: ",
            "Доступные атаки: ",
        ]
        
        frame_layout.addStretch()"""

{
                    "tag": player.tag,
                    "name": player.name,
                    "cg_value": 0,
                    "CCcontributions_value": player.donations,
                    "CCrecieved": player.received,
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
                }


async def main():
    try:
        datagetter = DataGetter()
        await datagetter.login(APILogin, APIPassword)

        app = QApplication(sys.argv)

        # Создаем цикл событий qasync
        loop = QEventLoop(app)
        asyncio.set_event_loop(loop)

        window = MainWindow()

        @asyncSlot()
        async def on_member_selected(membertag):
            try:
                member_data = await datagetter.on_member_selected(membertag)
                if member_data:
                    window.populate_player_frame(member_data)
                else:
                    print(f"Игрок {membertag} не найден")
            except Exception as e:
                print(f"Ошибка при получении данных игрока: {e}")
                import traceback
                traceback.print_exc()

        window.member_selected.connect(on_member_selected)

        window.show()

        members = await datagetter.getClanMembers_byclantag(Clantag)
        mbrs_activity = create_activity_list(len(members))
        window.populate_members_table(members, mbrs_activity)

        with loop:
            loop.run_forever()

    finally:
        await datagetter.logout()

if __name__ == "__main__":
        # Создаем новый цикл событий
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        # Запускаем основную функцию
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("Программа остановлена пользователем")
    finally:
        # Закрываем цикл
        loop.close()