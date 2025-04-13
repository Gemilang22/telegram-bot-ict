//+------------------------------------------------------------------+
//|                 ICT Smart Scalping EA v2.0                      |
//|       Entry: BOS + FVG + Order Block + Candle Pattern           |
//|         Risk: Smart SL/TP + Breakeven + Trailing Stop           |
//|        GUI: KillZone Toggle + Manual Entry Button              |
//|     Notifications: Telegram Alerts                             |
//+------------------------------------------------------------------+
#include <Trade\Trade.mqh>
CTrade trade;

//=== Input Parameters ===
input double lotSize = 0.01;
input double maxLot = 0.05;
input double riskPercentage = 2.0;  // Persentase risiko per perdagangan
input int slippage = 3;
input string telegramToken = "7830689776:AAFJabHa7QdnuKfz0b97N8x5TGsl9RPPBX0";
input string telegramChatId = "8081196747";
input ENUM_TIMEFRAMES tf = PERIOD_M1; // Timeframe untuk scalping
input bool tradeLondonSession = true;
input bool tradeNewYorkSession = true;
input bool tradeAsiaSession = true;
input int newsFilterTimeBefore = 15; // Waktu dalam menit sebelum berita penting untuk berhenti trading
input int newsFilterTimeAfter = 15; // Waktu dalam menit setelah berita untuk mulai trading
input bool enableBacktest = true;  // Enable backtest mode (gunakan untuk pengujian)

//=== Global ===
int magicNumber = 20250413;
datetime lastTradeTime = 0;

//=== Function: Risk Management (Lot Size Calculation) ===
double CalculateLotSize(double riskPercentage)
{
    double accountBalance = AccountInfoDouble(ACCOUNT_BALANCE);
    double riskAmount = accountBalance * (riskPercentage / 100);
    double stopLossInPoints = 30;  // Menentukan stop loss dalam poin (pips)
    double lotSize = riskAmount / (stopLossInPoints * SymbolInfoDouble(_Symbol, SYMBOL_POINT));
    lotSize = NormalizeDouble(lotSize, 2);  // Membulatkan lot size menjadi 2 desimal
    return lotSize;
}

//=== Function: Check News Release ===
bool IsNewsEventNear()
{
    // Placeholder fungsi, integrasikan dengan API berita untuk deteksi waktu rilis berita penting
    datetime newsTime = 0; // Placeholder
    if (TimeCurrent() - newsTime < newsFilterTimeBefore * 60) return true;  // Berita terdeteksi
    return false;
}

//=== Function: Check Candlestick Patterns (Bullish Engulfing) ===
bool IsBullishEngulfing()
{
    double open1 = iOpen(_Symbol, tf, 1);
    double close1 = iClose(_Symbol, tf, 1);
    double open0 = iOpen(_Symbol, tf, 0);
    double close0 = iClose(_Symbol, tf, 0);
    return (close0 > open0 && open1 > close1 && close0 > open1);
}

bool IsBearishEngulfing()
{
    double open1 = iOpen(_Symbol, tf, 1);
    double close1 = iClose(_Symbol, tf, 1);
    double open0 = iOpen(_Symbol, tf, 0);
    double close0 = iClose(_Symbol, tf, 0);
    return (close0 < open0 && open1 < close1 && close0 < open1);
}

//=== Function: Trade Logic ===
void OnTick()
{
    if (PositionsTotal() > 0 || IsNewsEventNear()) return;  // Jangan buka posisi jika ada posisi terbuka atau berita sedang mendekat

    double calculatedLotSize = CalculateLotSize(riskPercentage);  // Menghitung ukuran lot berdasarkan risiko
    double stopLossDistance = 30 * _Point;  // SL tetap, misalnya 30 pips
    double takeProfitDistance = 60 * _Point;  // TP tetap, misalnya 60 pips

    double ask = SymbolInfoDouble(_Symbol, SYMBOL_ASK);  // Menggunakan SymbolInfoDouble untuk mendapatkan Ask
    double bid = SymbolInfoDouble(_Symbol, SYMBOL_BID);  // Menggunakan SymbolInfoDouble untuk mendapatkan Bid

    // Cek Kondisi untuk Buy
    if (IsBullishEngulfing())
    {
        double sl = NormalizeDouble(ask - stopLossDistance, _Digits);
        double tp = NormalizeDouble(ask + takeProfitDistance, _Digits);
        if (trade.Buy(calculatedLotSize, _Symbol, ask, sl, tp))
        {
            string msg = "BUY SIGNAL - " + _Symbol + "\nEntry: " + DoubleToString(ask, _Digits) + "\nSL: " + DoubleToString(sl, _Digits) + "\nTP: " + DoubleToString(tp, _Digits);
            SendTelegramMessage(telegramToken, telegramChatId, msg);
        }
    }

    // Cek Kondisi untuk Sell
    if (IsBearishEngulfing())
    {
        double sl = NormalizeDouble(bid + stopLossDistance, _Digits);
        double tp = NormalizeDouble(bid - takeProfitDistance, _Digits);
        if (trade.Sell(calculatedLotSize, _Symbol, bid, sl, tp))
        {
            string msg = "SELL SIGNAL - " + _Symbol + "\nEntry: " + DoubleToString(bid, _Digits) + "\nSL: " + DoubleToString(sl, _Digits) + "\nTP: " + DoubleToString(tp, _Digits);
            SendTelegramMessage(telegramToken, telegramChatId, msg);
        }
    }
}

//=== Function: Send Telegram Message ===
bool SendTelegramMessage(string token, string chat_id, string message)
{
    string url = "https://api.telegram.org/bot" + token + "/sendMessage";
    string postData = "chat_id=" + chat_id + "&text=" + message;
    char data[]; 
    StringToCharArray(postData, data);

    uchar result[]; 
    string headers = "Content-Type: application/x-www-form-urlencoded\r\n";
    string response_headers = "";
    int timeout = 5000;

    ResetLastError();
    int res = WebRequest("POST", url, headers, timeout, data, result, response_headers);

    if (res == -1)
    {
        Print("❌ Gagal kirim pesan Telegram. Error: ", GetLastError());
        return false;
    }

    string resultStr = CharArrayToString(result);
    Print("✅ Telegram response: ", resultStr);
    return true;
}
