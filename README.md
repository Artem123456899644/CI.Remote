# CI.Remote

CI.Remote — это проект для удаленного контроля и обновления приложений, написанный на Python. Он позволяет управлять запущенными скриптами, обновлять приложения и мониторить состояние сервера через Telegram-бота.

## Возможности

1. **Удалённый контроль**: запуск, контроль, остановка и перезапуск скриптов через Telegram.
2. **Обновление приложений**: загрузка новых версий и их автоматическая установка.
3. **Мониторинг состояния**: получение информации о загруженности системы, логах работы скриптов и прочем.
4. **Автозагрузка и обновление**: автоматическое скачивание новых скриптов из облака и их интеграция в систему.

## Суть работы

Этот инструмент управляет процессами. Каждый скрипт запускается как отдельный процесс, а взаимодействие с ним происходит через стандартные потоки ввода-вывода.
- **Приём команд** осуществляется через `sys.stdin()`.
- **Вывод информации** происходит через `print()`.
- Форматы вывода:
  1. `__send`: сообщение выводится в Telegram-бота.
  2. `__log`: сообщение записывается в логи (начиная с версии 0.2).

### Реестр команд
При обнаружении нового скрипта в облаке он автоматически скачивается (опционально), после чего проходит проверку:
1. Наличие команд (`commands`)
2. Версия (`version`)

После этого скрипт добавляется в реестр (`info/scriptbase.json`) и становится доступным для использования через бота. В проект включён пример скрипта **Wake on LAN** с вымышленными MAC-адресами.

## Зависимости
Для работы необходимо установить следующие библиотеки:
1. `yadisk`
2. `asyncio`
3. `json5`
4. `aiogram`
5. `importlib`
6. `inspect`

## Начало работы
Для настройки CI.Remote необходимо заполнить файл `kap.json`. В текущей версии поддерживается только облачное хранилище [drive.yandex.ru](https://drive.yandex.ru). При необходимости можно интегрировать другие системы синхронизации.

## ВНИМАНИЕ
Проект имеет ряд недостатков, которые могут привести к серьёзным последствиям:
1. **Отсутствие механизмов безопасности** — нет шифрования и защиты данных.
2. **Ограниченный функционал** — проект находится в стадии разработки и будет совершенствоваться со временем.
3. **Отсутствие полноценного логирования** — несмотря на подготовку к этой функции, пока что логи необходимо фиксировать вручную.

