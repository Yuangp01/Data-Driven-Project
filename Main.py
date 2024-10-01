import pandas as pd

table_data = {'Team': ['Real Madrid','Barcelona', 'Girona','Athletic Club','Atletico Madrid','Real Sociedad','Betis','Valencia','Villarreal','Getafe','Las Palmas','Osasuna','Alaves','Mallorca','Rayo.V','Sevilla','Celta Vigo','Cadiz','Granada','Almeria'],
              'PJ': [29,29,28,29,29,29,29,28,29,29,29,29,29,29,29,29,29,29,28,29],
              'PG': [22,19,19,16,17,12,10,11,10,9,10,10,8,6,6,6,6,3,2,1],
              'PE': [6,7,5,8,4,10,12,7,8,11,7,6,8,12,11,10,9,13,8,10],
              'PP': [1,3,5,5,8,7,7,10,11,9,12,13,13,11,12,13,14,13,18,18],
              'GF': [64,60,59,50,54,42,34,32,47,37,29,33,26,25,25,36,32,20,30,28],
              'GC': [20,34,34,26,34,31,33,32,51,42,32,43,35,35,38,44,44,40,58,57],
              'DG': [44,26,25,24,20,11,1,0,-4,-5,-3,-10,9,-10,-13,-8,-12,-20,-28,-29],
              'Points': [72,64,62,56,55,46,42,40,38,38,37,36,32,30,29,28,27,22,14,13]
              }
table_df = pd.DataFrame(table_data)
file_path = 'classification.xlsx'


# Create a test DataFrame and save it as an Excel file
clashes_data = {'Real Madrid': ['Athletic Club','Mallorca','Barcelona','Real Sociedad','Cadiz','Granada','Alaves','Villarreal','Betis',''],
                'Barcelona': ['Las Palmas','Cadiz','Real Madrid','Valencia','Girona','Real Sociedad','Almeria','Rayo.V','Sevilla',''],
                'Girona': ['Betis','Athletic Club','Cadiz','Las Palmas','Barcelona','Alaves','Villarreal','Valencia','Granada',''],
                'Athletic Club': ['Real Madrid','Villarreal','Granada','Atletico Madrid','Getafe','Osasuna','Celta Vigo','Sevilla','Rayo.V',''],
                'Atletico Madrid': ['Villarreal','Girona','Alaves','Athletic Club','Mallorca','Celta Vigo','Getafe','Osasuna','Real Sociedad',''],
                'Real Sociedad': ['Alaves','Almeria','Getafe','Real Madrid','Las Palmas','Barcelona','Valencia','Betis','Atletico Madrid',''],
                'Betis': ['Girona','Celta Vigo','Valencia','Sevilla','Osasuna','Almeria','Las Palmas','Real Sociedad','Real Madrid',''],
                'Valencia': ['Mallorca','Granada','Osasuna','Betis','Barcelona','Alaves','Rayo.V','Real Sociedad','Girona','Celta Vigo'],
                'Villarreal': ['Atletico Madrid','Athletic Club','Almeria','Rayo.V','Celta Vigo','Sevilla','Girona','Real Madrid','Osasuna',''],
                'Getafe': ['Sevilla','Rayo.V','Real Sociedad','Almeria','Athletic Club','Cadiz','Atletico Madrid','Alaves','Mallorca',''],
                'Las Palmas': ['Barcelona','Sevilla','Celta Vigo','Girona','Real Sociedad','Mallorca','Betis','Cadiz','Alaves',''],
                'Osasuna': ['Almeria','Valencia','Rayo.V','Granada','Betis','Athletic Club','Mallorca','Atletico Madrid','Villarreal',''],
                'Alaves': ['Real Sociedad','Granada','Atletico Madrid','Celta Vigo','Valencia','Girona','Real Madrid','Getafe','Las Palmas',''],
                'Mallorca': ['Valencia','Real Madrid','Sevilla','Cadiz','Atletico Madrid','Las Palmas','Osasuna','Almeria','Getafe',''],
                'Rayo.V': ['Celta Vigo','Getafe','Osasuna','Villarreal','Almeria','Valencia','Granada','Barcelona','Athletic Club',''],
                'Sevilla': ['Getafe','Las Palmas','Mallorca','Betis','Granada','Villarreal','Cadiz','Athletic Club','Barcelona',''],
                'Celta Vigo': ['Rayo.V','Betis','Las Palmas','Alaves','Villarreal','Atletico Madrid','Athletic Club','Granada','Valencia',''],
                'Cadiz': ['Granada','Barcelona','Girona','Mallorca','Real Madrid','Getafe','Sevilla','Las Palmas','Almeria',''],
                'Granada': ['Cadiz','Valencia','Alaves','Athletic Club','Osasuna','Sevilla','Real Madrid','Rayo.V','Celta Vigo','Girona'],
                'Almeria': ['Osasuna','Real Sociedad','Villarreal','Getafe','Rayo.V','Betis','Barcelona','Mallorca','Cadiz','']
                }
clashes_df = pd.DataFrame(clashes_data)

with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
    table_df.to_excel(writer, sheet_name='Table', index=False)
    clashes_df.to_excel(writer, sheet_name='Clashes', index=False)