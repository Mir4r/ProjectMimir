#Statistical tools for Mimir
#2016, K Schweiger
import sys
import os
from glob import glob

import numpy as np
import seaborn as sns; sns.set(color_codes=True)
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd

import backend
import sharedfunctions


class statistics:
    def __init__( self , directory ):
        backupDBFiles = glob(directory+".mimir/main.db*.backup")
        backupDBFiles.sort()
        self.DBs = {}
        self.DBKeys = []
        for iDB, BackupDB in enumerate(backupDBFiles):
            print BackupDB
            name = BackupDB.split("/")
            name = "20"+name[-1][len("main.db-"):-len(".backup")]
            name = name.replace(".","-")
            self.DBKeys.append(name)
            self.DBs.update( { name : backend.database(2,directory,BackupDB) } )
            if iDB is 10:
                pass

    # Build DataFrames form backuped data
    def BuildDataFrame(self):
        self.SpecDFs = { "STUDIO" : pd.DataFrame() ,
                         "INTERPRET" : pd.DataFrame(),
                         "GENRE" : pd.DataFrame()} 
        entries = []
        neveropened = []
        for key in self.DBKeys:
            Specs = self.DBs[key].getListofSpecs(["STUDIO","INTERPRET","GENRE"])
            for dict_key in Specs.keys():
                df = pd.DataFrame()
                df = df.from_dict(Specs[dict_key], orient='index')
                df.rename(columns={0:key}, inplace = True)
                if self.SpecDFs[dict_key].empty:
                    self.SpecDFs[dict_key] = df
                else:
                    self.SpecDFs[dict_key] = self.SpecDFs[dict_key].join(df, how='outer')
            entries.append( self.DBs[key].getnumberofentrys() )
            neveropened.append( len(self.DBs[key].getbytimesopened("0")) )
        data = { 'Date' : self.DBKeys , 
                 'Entries' : entries ,
                 'NeverOpened' : neveropened }
        self.df = pd.DataFrame(data)
        self.df.set_index('Date', inplace = True)        
        self.SpecDFs["STUDIO"].index.name = "Studio"
        self.SpecDFs["GENRE"].index.name = "Genre"
        self.SpecDFs["INTERPRET"].index.name = "Interpret"
        self.SpecDFs["STUDIO"].fillna(0, inplace=True)
        self.SpecDFs["GENRE"].fillna(0, inplace=True)
        self.SpecDFs["INTERPRET"].fillna(0, inplace=True)
        # Save percentage based DataFrames
        # Divide by total number of studios, because the percentage of entries with spec are desired
        self.SpecDFs_percentage = { "STUDIO"     : self.SpecDFs["STUDIO"].divide( self.SpecDFs["STUDIO"].sum() ),
                                    "GENRE"      : self.SpecDFs["GENRE"].divide( self.SpecDFs["GENRE"].sum() ),
                                    "INTERPRET"  : self.SpecDFs["INTERPRET"].divide( self.SpecDFs["INTERPRET"].sum() ) }
        self.SpecDFs_percentage_ofEntries = { "STUDIO"     : self.SpecDFs["STUDIO"].divide( self.SpecDFs["STUDIO"].sum() ),
                                              "GENRE"      : self.SpecDFs["GENRE"].divide( self.SpecDFs["STUDIO"].sum() ),
                                              "INTERPRET"  : self.SpecDFs["INTERPRET"].divide( self.SpecDFs["STUDIO"].sum() ) }

    # Plot pie chart for a column of a DataFrame, drop NaN values and only keep rows with values over threshold
    # Standard setting are for a DataFrame with percentages of total number.
    def PlotPieChart( self, DataFrame, column, threshold = 0.01, label = "Others" , title=""):
        fig = plt.figure()
        fig.suptitle(title)
        ax = fig.add_subplot(111)
        # Get Series to plot
        series = DataFrame[column]
        # Drop NaN values
        series = series.dropna()
        # Drop values with less than threshold percentage of total number
        for index in series.index.values:
            if series[index] <= threshold:
                series = series.drop(index)
        # Add the dropped percentages to the series
        series = series.append(pd.Series( [ 1 - series.sum() ], index = [label]) )
        series.plot(kind="pie", ax = ax)
        return fig
        
    # Plot the time progression of all specs. A threshold can be defined if not all specs should be plotted.    
    def PlotSpecHistory( self, DataFrame, nSubItems = 5, indexedbyDate = False, ascendingorder = False, tothreshold = None, title = "" ):
        returnlist = []
        sorted_list = self.GetSortedIndexList( DataFrame, indexedbyDate, ascendingorder,tothreshold )
        sorted_divided_list = [sorted_list[i:i+nSubItems] for i in range(0, len(sorted_list), nSubItems)]
        for sublist in  sorted_divided_list:
            fig = plt.figure()
            fig.suptitle(title)
            ax = fig.add_subplot(111)
            if indexedbyDate is False:
                DataFrame.transpose().plot(y = sublist, legend = True, ax=ax)
            else:
                DataFrame.plot(y = sublist, legend = True, ax=ax)
            ax.set_xlabel("Date")
            ax.set_ylabel("Share of entries with spec [%]")
            returnlist.append(fig)
        return returnlist

    def PlotDataFrame( self, DataFrame ):
        fig = plt.figure()
        ax1 = plt.subplot2grid( (6,1) , (0,0) , rowspan=2 , colspan=1 )
        ax2 = plt.subplot2grid( (6,1) , (2,0) , rowspan=4 , colspan=1 )

        DataFrame.plot(ax=ax2)
        DataFrame.pct_change().plot(ax=ax1,legend = False)
        ax1.get_xaxis().set_ticklabels([])
        ax1.set_xlabel("")
        ax1.locator_params(tight=True, nbins=4,axis='y')
        #        figure.axes.append(ax)
        return fig

    # Return a list of indexes sorted by total share of latest dataset
    def GetSortedIndexList( self, DataFrame, indexedbyDate = False, ascendingorder = False , tothreshold = None ):
        # Get List of all specs in ever present in all datasets 
        if not indexedbyDate:
            column_name = DataFrame.transpose().index.values[-1]
        else:
            column_name = DataFrame.index.values[-1]
        sorted_df = DataFrame.sort_values(column_name,ascending=ascendingorder)
        fulllist = sorted_df.index.values    # This list contains all Specs
        # For plotting it can be usefull, to only plot specs with more share than a threshold
        if tothreshold is not None:
            for i, index  in enumerate(fulllist):
                if not ascendingorder:
                    if sorted_df.get_value(index,column_name) < tothreshold:
                        returnlist = fulllist[0:i]
                        break
                else:
                    if sorted_df.get_value(index,column_name) > tothreshold:
                        returnlist = fulllist[i:]
                        break
        else:
            returnlist = fulllist
        return returnlist
    
    # Plotting function for class
    def Plot(self):
        mainplot = self.PlotDataFrame(self.df)
        PieChart_latest_Studio = self.PlotPieChart( self.SpecDFs_percentage["STUDIO"], self.DBKeys[-1] , threshold = 0.005)
        PieChart_latest_Genre = self.PlotPieChart( self.SpecDFs_percentage["GENRE"], self.DBKeys[-1] )
        TS_genre_list = self.PlotSpecHistory( self.SpecDFs_percentage_ofEntries["GENRE"], tothreshold = 0.03, title = "Genres")
        TS_studio_list = self.PlotSpecHistory( self.SpecDFs_percentage_ofEntries["STUDIO"], tothreshold = 0.005, title = "Studios")
        with PdfPages('Statistics_output.pdf') as pdf:
            pdf.savefig(mainplot)
            #    pdf.savefig(mainplot_pct_change)
            for plot in TS_genre_list+TS_studio_list:
               pdf.savefig(plot) 
            pdf.savefig(PieChart_latest_Studio)
            pdf.savefig(PieChart_latest_Genre)

           
def main():
    stats = statistics("/media/truecrypt12/Video/")
    stats.BuildDataFrame()
    stats.Plot()
    
if __name__ == '__main__':
    main()
