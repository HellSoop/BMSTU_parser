START_TEMPLATE = ('Приветствую! Теперь я буду присылать Вам <b>уведомления'
                  ' о важных новостях во всех бауманских каналах</b>. '
                  'Используйте <b>/help</b>, если хотите узнать, что я могу.')

HELP_TEMPLATE = ('<u><b>Список доступных команд:</b></u>\n'
                 '<b>/help</b> - <i>Вывести список доступных команд</i>\n'
                 '<b>/start</b> - <i>Включить рассылку важных новостей</i>\n'
                 '<b>/stop</b> - <i>Выключить рассылку важных новостей</i>\n'
                 '<b>/history</b> - <i>Посмотреть историю по каналам</i>\n'
                 '<b>/subscriptions</b> - <i>Управление подписками</i>')

STOP_TEMPLATE = 'Вы отключили рассылку новостей. Вы всегда можете включить её обратно, при помощи команды <b>/start</b>'

SUBSCRIPTIONS_NOT_REGISTERED_TEMPLATE = ('Чтобы редактировать список подписок <b>необходимо включить '
                                         'рассылку новостей</b>.\nВы можете сделать это c помощью команды'
                                         ' <b>/start</b>')
