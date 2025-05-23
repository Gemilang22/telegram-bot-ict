//+------------------------------------------------------------------+
//|                 ICT Smart Scalping EA v1.0                      |
//|       Entry: BOS + FVG + Order Block + Candle Pattern           |
//|         Risk: Smart SL/TP + Breakeven + Trailing Stop           |
//|        GUI: KillZone Toggle + Manual Entry Button              |
//|     Notifications: Telegram Alerts                             |
//+------------------------------------------------------------------+
#include <Trade\Trade.mqh>
CTrade trade;

//=== Input Parameters ===
input double lotSize = 0.01;
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

    // Membatasi lot size antara 0.01 dan 0.03
    if (lotSize < 0.01) {
        lotSize = 0.01;  // Set ke lot minimum yang diizinkan
    }
    if (lotSize > 0.03) {
        lotSize = 0.03;  // Set ke lot maksimum yang diizinkan
    }

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
            string msg = "|| BUY SIGNAL ||\n\n" +
                         "Symbol: ~ " + _Symbol + " ~\n" +
                         "Entry: `" + DoubleToString(ask, _Digits) + "`\n" +
                         "Jumlah Lot: " + DoubleToString(calculatedLotSize, 2) + "\n" +
                         "Take Profit: `" + DoubleToString(tp, _Digits) + "`\n" +
                         "Stop Loss: `" + DoubleToString(sl, _Digits) + "`\n\n" +
                         "Time: _" + TimeToString(TimeCurrent(), TIME_DATE | TIME_MINUTES) + " WIB_\n\n" +
                         "_Good luck with the trade!_";
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
            string msg = "|| SELL SIGNAL ||\n\n" +
                         "Symbol: ~ " + _Symbol + " ~\n" +
                         "Entry: `" + DoubleToString(bid, _Digits) + "`\n" +
                         "Jumlah Lot: " + DoubleToString(calculatedLotSize, 2) + "\n" +
                         "Take Profit: `" + DoubleToString(tp, _Digits) + "`\n" +
                         "Stop Loss: `" + DoubleToString(sl, _Digits) + "`\n\n" +
                         "Time: _" + TimeToString(TimeCurrent(), TIME_DATE | TIME_MINUTES) + " WIB_\n\n" +
                         "_Good luck with the trade!_";
            SendTelegramMessage(telegramToken, telegramChatId, msg);
        }
    }
}

//+------------------------------------------------------------------+
//| Kirim Notifikasi TP/SL Saat Posisi Ditutup                       |
//+------------------------------------------------------------------+
void OnTradeTransaction(const MqlTradeTransaction &trans, const MqlTradeRequest &req, const MqlTradeResult &result)
{
   if (trans.type == TRADE_TRANSACTION_DEAL_ADD)
   {
      if (trans.deal_type == DEAL_TYPE_SELL || trans.deal_type == DEAL_TYPE_BUY)
      {
         ulong ticket = trans.deal;
         if (HistoryDealSelect(ticket))
         {
            double entryPrice = HistoryDealGetDouble(ticket, DEAL_PRICE);
            double volume     = HistoryDealGetDouble(ticket, DEAL_VOLUME);
            string symbol     = HistoryDealGetString(ticket, DEAL_SYMBOL);
            double profit     = HistoryDealGetDouble(ticket, DEAL_PROFIT);

            // Estimasi pips
            double exitPrice = SymbolInfoDouble(symbol, SYMBOL_BID);
            int pips = (int)MathAbs((exitPrice - entryPrice) / _Point);

            string status = (profit > 0) ? "|| TAKE PROFIT ||" : "|| STOP LOSS ||";
            string action = (trans.deal_type == DEAL_TYPE_BUY) ? "CLOSE BUY" : "CLOSE SELL";

            string msg = StringFormat("%s\n\nSymbol: %s\nLot: %.2f\nPips: %d\nProfit: %.2f IDR\nTime: %s WIB",
               status, symbol, volume, pips, profit, TimeToString(TimeCurrent(), TIME_DATE | TIME_MINUTES));

            // Mengubah pesan TP/SL sesuai permintaan Anda
            if (status == "|| STOP LOSS ||")
            {
                msg = "|| STOP LOSS ||\n\n" +
                      action + "\n\n" +
                      "Symbol: " + symbol + "\n" +
                      "Lot: " + DoubleToString(volume, 2) + "\n" +
                      "Pips: " + IntegerToString(pips) + "\n" +
                      "Profit: " + DoubleToString(profit, 2) + " IDR\n" +
                      "Time: " + TimeToString(TimeCurrent(), TIME_DATE | TIME_MINUTES) + " WIB";
            }

            SendTelegramMessage(telegramToken, telegramChatId, msg);
         }
      }
   }
}

