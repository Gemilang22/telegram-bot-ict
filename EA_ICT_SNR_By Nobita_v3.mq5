//+------------------------------------------------------------------+
//| ICT Smart Scalping EA v2.1                                            |
//| Entry: Bullish/Bearish Engulfing                                      |
//| Risk: SL/TP Tetap, Notifikasi Telegram (TP/SL via OnTradeTransaction) |
//+------------------------------------------------------------------+
#property copyright "By Nobita"
#property version   "2.2"
#property strict

#include <Trade/Trade.mqh>
CTrade trade;

input double TakeProfitPips = 50;
input double StopLossPips   = 30;
input double LotSize        = 0.01;

string TelegramToken = "7830689776:AAFJabHa7QdnuKfz0b97N8x5TGsl9RPPBX0";
string TelegramChatID = "8081196747";

datetime lastEntryTime = 0;



//+------------------------------------------------------------------+
//| Fungsi Kirim Pesan Telegram                                      |
//+------------------------------------------------------------------+
void SendTelegramMessage(string message)
{
   string url = "https://api.telegram.org/bot" + TelegramToken + "/sendMessage";
   string post = "chat_id=" + TelegramChatID + "&text=" + message;
   
   char post_data[];
   StringToCharArray(post, post_data);

   char result[];
   string headers;
   string response_headers;
   int timeout = 5000;

   ResetLastError();
   int res = WebRequest(
      "POST",
      url,
      headers,
      timeout,
      post_data,
      result,
      response_headers
   );

   if (res == -1)
      Print("WebRequest error: ", GetLastError());
   else
      Print("Telegram message sent: ", message);
}


//+------------------------------------------------------------------+
//| Format tanggal dan waktu 24 jam                                 |
//+------------------------------------------------------------------+
string GetDateTimeString()
{
   MqlDateTime dt;
   TimeToStruct(TimeLocal(), dt);
   string bulan[] = {"Januari", "Februari", "Maret", "April", "Mei", "Juni",
                     "Juli", "Agustus", "September", "Oktober", "November", "Desember"};
   return StringFormat("%d %s %d, pukul %02d:%02d WIB", dt.day, bulan[dt.mon - 1], dt.year, dt.hour, dt.min);
}

//+------------------------------------------------------------------+
//| Fungsi Entry Order                                               |
//+------------------------------------------------------------------+
void CheckSignalAndEntry()
{
   double bid = SymbolInfoDouble(_Symbol, SYMBOL_BID);
   double ask = SymbolInfoDouble(_Symbol, SYMBOL_ASK);

   // Contoh sinyal engulfing
   double open1 = iOpen(_Symbol, PERIOD_M1, 1);
   double close1 = iClose(_Symbol, PERIOD_M1, 1);
   double open2 = iOpen(_Symbol, PERIOD_M1, 2);
   double close2 = iClose(_Symbol, PERIOD_M1, 2);

   if (TimeCurrent() - lastEntryTime < 60) return; // hindari spam

   if (close2 < open2 && close1 > open1 && close1 > open2 && open1 < close2)
   {
      double sl = NormalizeDouble(bid - (StopLossPips * _Point), _Digits);
      double tp = NormalizeDouble(bid + (TakeProfitPips * _Point), _Digits);

      if (trade.Buy(LotSize, _Symbol, bid, sl, tp))
      {
         lastEntryTime = TimeCurrent();
         string msg = StringFormat(
            "|| BUY SIGNAL ||\n\nSymbol: ~ %s ~\nEntry: `%.2f`\njumlah lot : %.2f\nTake Profit: `%.2f` (%d pips)\nStop Loss: `%.2f` (%d pips)\n\nTime: %s\n\nGood luck with the trade!",
            _Symbol, bid, LotSize, tp, (int)TakeProfitPips, sl, (int)StopLossPips, GetDateTimeString());
         SendTelegramMessage(msg);
      }
   }
   else if (close2 > open2 && close1 < open1 && close1 < open2 && open1 > close2)
   {
      double sl = NormalizeDouble(ask + (StopLossPips * _Point), _Digits);
      double tp = NormalizeDouble(ask - (TakeProfitPips * _Point), _Digits);

      if (trade.Sell(LotSize, _Symbol, ask, sl, tp))
      {
         lastEntryTime = TimeCurrent();
         string msg = StringFormat(
            "|| SELL SIGNAL ||\n\nSymbol: ~ %s ~\nEntry: `%.2f`\njumlah lot : %.2f\nTake Profit: `%.2f` (%d pips)\nStop Loss: `%.2f` (%d pips)\n\nTime: %s\n\nGood luck with the trade!",
            _Symbol, ask, LotSize, tp, (int)TakeProfitPips, sl, (int)StopLossPips, GetDateTimeString());
         SendTelegramMessage(msg);
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

            string msg = StringFormat("%s\n\nSymbol: %s\nLot: %.2f\nPips: %d\nProfit: %.2f USD\nTime: %s",
               status, symbol, volume, pips, profit, GetDateTimeString());

            SendTelegramMessage(msg);
         }
      }
   }
}

//+------------------------------------------------------------------+
//| OnTick                                                           |
//+------------------------------------------------------------------+
void OnTick()
{
   CheckSignalAndEntry();
}
