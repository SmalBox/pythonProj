
webDriverOffJs = '''() =>{
    Object.defineProperties(navigator,{
        webdriver:{
          get: () => false
        }
    })}
'''

intervalCallTest = '''
    for (let index = 1; index < 9; index++) {
        setTimeout(getOldHouse(vars,index), 3000)
    }
'''