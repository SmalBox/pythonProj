# PyReg V0.1

## Description
   
   - Python **正则表达式** 文本替换工具
   - 可以对文本文件使用[符合python的正则表达式规则](https://docs.python.org/zh-cn/3/library/re.html)，做文本替换处理。

## Usage

   1. 终端中输入 “python ./PyReg.py” 进入程序
   2. 按照提示依次输入**文件路径**、**正则表达式**、**要替换成的字符**
   3. 程序会显示**源文件内容**和**替换完的内容**，并询问是否写入文件
   4. 完成一次替换后，会询问是否退出，如果不选择退出，会再次提示输入文件路径、正则表达式、要替换成的字符

   - **Example**
      ``` bash
      $ python ./regular.py
      ========Start Regular=========
      Enter File Path: test.md
      Enter Regular: 123
      Enter Replaced String: 0
      =====File Read Completed======
      
      ▼▼▼▼File Original Content:▼▼▼▼
      # test replaced (替换)
      abc123
      ### title test-doc (测试标题)
      
      ▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲
      
      ▼▼▼▼▼▼▼Replaced result:▼▼▼▼▼▼▼
      # test replaced (替换)
      abc0
      ### title test-doc (测试标题)
      
      ▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲
      
      Match 1 place!
      Yes or No Write?
      Please enter Y or N: y
      =======Write Completed========
      Yes or No Exit?
      Please enter Y or N: n
      ========Start Regular=========
      Enter File Path: test.md
      Enter Regular: 0
      Enter Replaced String: 123
      =====File Read Completed======
      
      ▼▼▼▼File Original Content:▼▼▼▼
      # test replaced (替换)
      abc0
      ### title test-doc (测试标题)
      
      ▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲
      
      ▼▼▼▼▼▼▼Replaced result:▼▼▼▼▼▼▼
      # test replaced (替换)
      abc123
      ### title test-doc (测试标题)
      
      ▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲
      
      Match 1 place!
      Yes or No Write?
      Please enter Y or N: y
      =======Write Completed========
      Yes or No Exit?
      Please enter Y or N: y
      =========End Regular==========
      ```

