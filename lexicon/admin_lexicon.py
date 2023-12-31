COMMANDS: dict[dict[str: str]] = {
    'start_buttons': {'add_record': 'Записать клиента',
                      'client_list': 'Получить список клиентов',
                      'view_all_records': 'Посмотреть все доступные записи',
                      'remove_records': 'Посмотреть/Удалить запись на '
                                        'конкретную дату',
                      'add_service_button': 'Добавить услугу',
                      'remove_service_button': 'Удалить услугу'
                      }
}

MESSAGE: dict = {'enter_client_first_name': 'Введите имя клиента',
                 'enter_client_last_name': 'Введите фамилию клиента',
                 'enter_client_phone': 'Теперь введите номер телефона клиента без пробелов начиная с восьмерки',
                 'warning_client_not_first_name': 'Введенное имя некорректно, пожалуйста введите имя одним словом',
                 'warning_client_not_last_name': 'Введенная фамилия некорректна, пожалуйста введите фамилию одним словом',
                 'name_does_not_match': 'Этот телефон используется в базе для другого имени. Имя было заменено на '
                                        '{first_name} {last_name}',
                 'warning_client_not_phone': 'Телефон введен некорректно. Пожалуйста, введите номер телефона без '
                                             'пробелов начиная с 8. Пример: 89622555289',
                 'add_service_name': 'Пожалуйста, введите название услуги или нажмите кнопку '
                                     '"Отмена"',
                 'add_service_not_name': 'Это не похоже на название процедуры, введите название'
                                         ' с клавиатуры',
                 'add_service_duration': 'Теперь введите длительность процедуры в минутах',
                 'add_service_not_duration': 'Пожалуйста, введите длительность процедуры'
                                             ' в минутах целым числом без точки, запятой'
                                             ' или других символов',
                 'add_service_price': 'Теперь укажите цену услуги целым числом',
                 'add_service_not_price': 'Введите пожалуйста стоймость процедуры целым числом'
                                          ' без точки, запятой или других символов',
                 'add_service_description': 'Опционально. '
                                            'Теперь вы можете указать описание процедуры',
                 'add_service_incorrect_description': 'Описание указано неверно.'
                                                      ' Используйте текстовое поле для ввода'
                                                      ' сообщений, чтобы указать описание.'
                                                      ' Либо воспользуйтесь кнопками "Далее",'
                                                      ' "Отмена"',
                 'add_service_save_data': 'Спасибо! Новая услуга добавлена в перечень услуг',
                 'remove_service_message': 'Нажмите на кнопку услуги, которую нужно удалить',
                 'remove_not_service': 'Пожалуйста, нажмите на кнопку с услугой из списка услуг, '
                                       'чтобы удалить или нажмите "Отмена"',
                 'remove_service_success': 'Вы успешно удалили услугу из списка услуг',
                 'choice_date_message': 'Пожалуйста, выберите дату записи',
                 'choice_record_message': 'Список всех доступных записей на этот день. '
                                          'Нажмите на одну из них, если хотите удалить, '
                                          'либо нажмите "Отмена"',
                 'no_record_message': 'На эту дату еще нет записей, вы можете выбрать другую',
                 'record_deleted': 'Запись успешно удалена'
                 }
