# Analyzing-code-Metrics-2021

Team project to create a code analyzer for the discipline "System programming technology"
##Commit style  
Формат основного коммита:  
1)Что сделать + для какой сущности + подробности (необязательно)
  
    add ui-bootstrap.js dependency
	replace twitter-bootstrap.css with pure.css
	
2)Дополнительное сообщение - через строчку от основного  

	replace twitter-bootstrap.css with pure.css
	Made UI much cleaner.
	
3)Пишем сообщение с маленькой буквы

	add ui-bootstrap.js dependency
Вместо

	Add ui-bootstrap.js dependency
	
4)НЕ используем прошедшее время.
Чем проще, тем лучше.   Прошедшее время слишком усложняет чтение сообщений  

	add ui-bootstrap.js dependency
Вместо

	added ui-bootstrap.js dependency
	
5)Убираем лишние знаки препинания  

Формат информации идущей вместе с коммитом  
ДО основного коммита этого указываем тип коммита:  
   1. feature — используется при добавлении новой   функциональности уровня приложения  
   2. fix — если исправили какую-то серьезную багу  
   3. docs — всё, что касается документации  
   4. style — исправляем опечатки, исправляем форматирование  
   5. refactor — рефакторинг кода приложения  
   6. test — всё, что связано с тестированием  
   7. chore — обычное обслуживание кода  

И Указываем область действия (scope). Сразу после типа коммита без всяких
пробелов указываем в скобках область,   
на которую распространяется наш коммит.
После этого пишем наш стандартный коммит.

Кроме того, для интеграции с Jira нужно указывать
 COD-(номер вашего подзадания).
	
Итоговые коммиты выглядят:  

	COD-12 refactor(audio-controls) use common library for all controls
	COD-19 chore(Gruntfile.js) add watch task