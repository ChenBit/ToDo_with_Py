%1 mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c "^&chr(34)^&"%~0"^&chr(34)^&" ::","%cd%","runas",1)(window.close)&&exit

pip install -i https://pypi.tuna.tsinghua.edu.cn/simple flask
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple datetime
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple requests
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple flask_cors
