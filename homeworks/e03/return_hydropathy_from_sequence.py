import plotly.graph_objects as go
import pandas as pd
from collections import deque


aa_properties = pd.read_csv('/Users/huuumath/Git/fufezan-lab-advanced_python_2020-21_HD/data/amino_acid_properties.csv')

df_hydropathy = aa_properties.loc[:,['1-letter code', 'hydropathy index (Kyte-Doolittle method)']]


aa_hydropathy = {}
for index, row in df_hydropathy.iterrows():
    aa = row['1-letter code']
    hydropathy = row['hydropathy index (Kyte-Doolittle method)']

    aa_hydropathy[aa] = float(hydropathy)

# create topological domain
top_info = ['Extracellular']*31
top_info.extend(['Transmembrane']*26)
top_info.extend(['Cytoplasmic']*20)
top_info.extend(['Transmembrane']*18)
top_info.extend(['Extracellular']*10)
top_info.extend(['Transmembrane']*22)
top_info.extend(['Cytoplasmic']*22)
top_info.extend(['Transmembrane']*19)
top_info.extend(['Extracellular']*24)
top_info.extend(['Transmembrane']*23)
top_info.extend(['Cytoplasmic']*26)
top_info.extend(['Transmembrane']*24)
top_info.extend(['Extracellular']*22)
top_info.extend(['Transmembrane']*25)
top_info.extend(['Cytoplasmic']*49)

print(len(top_info))


def reading_the_fasta(fasta_file):
    '''
    '''
    seq = []
    with open(fasta_file, 'r') as fasta:
        for line in fasta:
            if line.startswith(">"):
                seq.append("")
            else:
                seq.append(line.strip("\n"))
    
    return("".join(seq))




fasta = reading_the_fasta('/Users/huuumath/Downloads/gpcr.fasta')


def map_hydropathy(protein_sequence, hydropathy_values):
    '''
    '''
    seq_hydropathy = []
    for aa in protein_sequence:
        seq_hydropathy.append(hydropathy_values[aa])

    return seq_hydropathy


def map_hydropathy_window(protein_sequence, hydropathy_values, len_sliding_window = None):
    '''
    '''
    seq_hydropathy = []
    for aa in protein_sequence:
        seq_hydropathy.append(hydropathy_values[aa])
    
    if len_sliding_window is not None:

        window = deque([], maxlen=len_sliding_window)
        seq_mean_hydropathy = []
        for pos, aa in enumerate(seq_hydropathy):
            window.append(aa)
            mean_window = sum(window)/len(window)
            seq_mean_hydropathy.append(mean_window)
        
        seq_hydropathy = seq_mean_hydropathy

    return seq_mean_hydropathy
    


def plot_lookup_hydropathy(
    value_list,
    topology,
    len_sliding_window):
    '''
    '''
    positions = range(1, (len(value_list)+1))

    df_plot = pd.DataFrame(
        {'Position': positions,
        'Hydropathy': value_list,
        'Topology': topology}
    )

    data = [
        go.Bar(
            x = df_plot['Position'],
            y = df_plot['Hydropathy'],
            marker_color = df_plot['Topology'].map(
                {
                    'Extracellular': 'green',
                    'Transmembrane': 'blue',
                    'Cytoplasmic': 'red'
                }
            )

        )
    ]
    fig = go.Figure(data=data)
    fig.layout.title.text = f'Hydropathy Lookup for G-Protein: P32249 with Sliding Window: {len_sliding_window}'.upper()
    fig.layout.title.font.size = 15
    fig.layout.xaxis.title = 'Protein Sequence Position'
    fig.layout.yaxis.title = 'Hydropathy'
    fig.show()


seq = reading_the_fasta('/Users/huuumath/Downloads/gpcr.fasta')

seq_hpi = map_hydropathy(seq, aa_hydropathy)
plot_lookup_hydropathy(
    value_list = seq_hpi,
    topology=top_info,
    len_sliding_window= 0)

seq_hpi_5 = map_hydropathy_window(seq, aa_hydropathy, 5)
plot_lookup_hydropathy(
    value_list=seq_hpi_5,
    topology= top_info,
    len_sliding_window=5
)

seq_hpi_15 = map_hydropathy_window(seq, aa_hydropathy, 15)
plot_lookup_hydropathy(
    value_list=seq_hpi_15,
    topology= top_info,
    len_sliding_window=15
)

seq_hpi_25 = map_hydropathy_window(seq, aa_hydropathy, 25)
plot_lookup_hydropathy(
    value_list=seq_hpi_25,
    topology=top_info,
    len_sliding_window=25
)

seq_hpi_35 = map_hydropathy_window(seq, aa_hydropathy, 35)
plot_lookup_hydropathy(
    value_list=seq_hpi_35,
    topology=top_info,
    len_sliding_window=35
)