import geopandas as gpd
import zipfile
import shapefile
import matplotlib.pyplot as plt
import pandas as pd
import os, re, sys

def mapmaker(path):
    """
        input: path to zip file with geodata
        output: map and number of unique zipcodes
    """

    zipped = zipfile.ZipFile(r'{}'.format(path), 'r')
    path = path = list(os.path.split(path))[0]
    zipped.extractall(r'{}\coordinates'.format(path))
    zipped.close()

    file = os.listdir(r'{}\coordinates'.format(path))[0]

    file = re.sub(r'\..+','.shp',file)

    df = gpd.read_file(r'{}/coordinates/{}'.format(path,file),encoding='cp1252')

    df['geostring'] = df['geometry'].astype(str)

    df.drop_duplicates(['geostring','POSTNUMMER'],inplace=True)

    print('Number of unique poscodes: '+ str(len(set(df['POSTNUMMER']))))
    
    df[['geometry','POSTNUMMER']].plot(figsize=(10,15)).axis('off')
    plt.savefig(r'{}\coordinates\postalcodes_map.png'.format(path),dpi=2000)
    plt.show()

if __name__ == "__main__":
    mapmaker(*sys.argv[1:])
