from datetime import datetime
import akshare as ak

import mplfinance as mpf
import pandas as pd
import os

from update_readme import update_readme


class SaveStockPlot(object):
    def __init__(self):
        self.fig_folder_name = 'fig'
        self.symbol_name = {
            'sh000001': '上证指数'
        }
        self.get_cur_time()
        self.prepare_fig_folder()

    def prepare_fig_folder(self):
        # current_file_path = os.path.abspath(__file__)
        # current_directory = os.path.join(os.path.dirname(current_file_path), self.fig_folder_name)
        current_directory = os.path.join('.', self.fig_folder_name)
        folder_path = os.path.join(current_directory, self.current_year, self.current_month)

        if not os.path.exists(folder_path):

            os.makedirs(folder_path)
        self.save_folder = folder_path

    def get_stock_data(self, symbol):
        self.symbol = symbol
        stock_df = ak.stock_zh_a_minute(symbol=symbol, period=1)

        stock_df['day'] = pd.to_datetime(stock_df['day'])
        stock_df.set_index('day', inplace=True)

        stock_df['open'] = pd.to_numeric(stock_df['open'], errors='coerce')
        stock_df['high'] = pd.to_numeric(stock_df['high'], errors='coerce')
        stock_df['low'] = pd.to_numeric(stock_df['low'], errors='coerce')
        stock_df['close'] = pd.to_numeric(stock_df['close'], errors='coerce')
        stock_df['volume'] = pd.to_numeric(stock_df['volume'], errors='coerce')
        return stock_df

    def get_cur_time(self):
        now = datetime.now()
        self.current_date = now.date().strftime("%Y%m%d")
        self.current_year = str(now.year)
        self.current_month = str(now.month)
        self.current_day = str(now.day)

        print("当前日期是:", self.current_date)
        # 将字符串日期转换为 pandas 的日期类型
        self.pd_current_date = pd.Timestamp(self.current_date)

    def get_today_data(self, df):
        # 使用布尔索引筛选数据
        mask = (df.index >= self.pd_current_date)
        filtered_df = df.loc[mask]
        return filtered_df

    def save_fig(self, df):
        kws = dict(volume=True, tight_layout=True)

        # 设置k线图颜色
        my_color = mpf.make_marketcolors(up='red',  # 上涨时为红色
                                         down='green',  # 下跌时为绿色
                                         edge='i',  # 隐藏k线边缘
                                         volume='in',  # 成交量用同样的颜色
                                         inherit=True)

        my_style = mpf.make_mpf_style(gridaxis='both',  # 设置网格
                                      gridstyle='-.',
                                      y_on_right=True,
                                      marketcolors=my_color)

        # title_name = self.current_date + ' ' + self.symbol_name[self.symbol]
        title_name = self.current_date
        fig_name = self.current_date + '-' + self.symbol + '.png'
        self.save_fig_path = os.path.join(self.save_folder, fig_name)

        mpf.plot(df.iloc[:, :],
                 **kws,
                 style=my_style,
                 type='hollow_and_filled',
                 mav=(5, 10, 30),
                 figratio=(1.5, 1),
                 figscale=3,
                 title=title_name,

                 savefig=self.save_fig_path)  # 新式的蜡烛图

    def process(self, symbol):

        self.prepare_fig_folder()
        df = self.get_stock_data(symbol)
        df = self.get_today_data(df)
        self.save_fig(df)
        return self.save_fig_path

    def run(self):
        sh_img_path = self.process('sh000001')
        sz_img_path = self.process('sz399001')
        bj_img_path = self.process('bj899050')

        update_readme(self.current_date, sh_img_path, sz_img_path, bj_img_path)


if __name__ == '__main__':
    ssp = SaveStockPlot()
    ssp.run()
