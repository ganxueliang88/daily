# daily
各种签到和airdop

## 准备
### 验证码 api key
充值并获得[2captcha](https://2captcha.com?from=12332166) 的 api key
在cofig 的 2captcha_apikey 部分填入这个api key

### bsc test faucet 配置
https://testnet.binance.org/faucet-smart
在cofig 的 bsc_test 部分配置 eth钱包地址和想要的货币
货币可选：  
* BNB
* BTC
* BUSD
* DAI
* ETH
* USDC
* USDT
* XRP
### goerli faucet  配置
https://faucet.goerli.mudit.blog/
在cofig 的 goerli  部分配置 twitter/facebook帖子地址，选择的执行类型

tier： 
- 0: 1eth/day,
- 1: 2.5eth/3day
- 2: 6.25/9day
### rinkeby faucet  配置
https://www.rinkeby.io/#faucet
在cofig 的 rinkeby  部分配置 twitter/facebook帖子地址，选择的执行类型

tier： 
- 0: 3eth/8h
- 1: 7.5eth/day
- 2: 18.75/3day

###  melos 配置
https://www.melos.studio/
在cofig 的 melos 部分配置 用户名和密码


## 运行配置
### github action 运行模式
- fork 项目 开启 github action
- 新建 repo secret: `CONFIG`，内容为刚刚修改好的配置文件
- 默认脚本每天北京时间8：30执行，可以按照需求自行修改

### 本地运行模式
```
python -m pip install -r requirements.txt
export CONFIG=`cat config/config.json`
python3 main.py
```

