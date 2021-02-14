import pandas as pd
from collections import deque
import requests
import plotly.graph_objects as go



class ProteinClass(object):
    ''' A Protein Class which can be initialized with different lookups (hydropathy e.g.).

    Attributes:
        name (str): Name of the Protein.
        sequence(str): The Aminoacid Sequence of the Protein.
        protein_id(str): The ID of the Protein (Uniprot Identifier).

    '''

    def __init__(self, name, sequence, protein_id):
        ''' Initialising the Properties of the Protein.
        Args:
            name (str): Name of the Protein.
            sequence(str): The Aminoacid Sequence of the Protein.
            protein_id(str): The ID of the Protein (Uniprot Identifier).
        '''

        self.name = name
        self.sequence = sequence
        self.protein_id = protein_id
    
    def get_data(self):
        ''' Get the Protein Sequence from Uniprot.

        Returns:
            The extracted Protein Sequence from Uniprot.

        '''

        url = f'https://www.uniprot.org/uniprot/{self.protein_id}.fasta?fil=reviewed:yes'
        r = requests.get(url)
        protein_csv = f'./data/{self.protein_id}.fasta'

        with open(protein_csv, 'wb') as file:
            file.write(r.content)
            file.close()
        
        
        seq = []
        with open(protein_csv, 'r') as fasta:
            for line in fasta:
                if line.startswith(">"):
                    seq.append("")
                else:
                    seq.append(line.strip("\n"))
    
        self.sequence = "".join(seq)



    def map(
        self, 
        aa_distribution_file = '/Users/huuumath/Git/fufezan-lab-advanced_python_2020-21_HD/data/amino_acid_properties.csv', 
        lookup = 'hydropathy index (Kyte-Doolittle method)', 
        len_sliding_window = None):
        ''' A Function which accepts a kwarg specifying which lookup should be used to map the sequence against

        Args:
            aa_distribution_file (str): A directory which points to the amino acid property file.
            lookup (str): Specifying the lookup.
            len_sliding_window (int): Length of the sliding window.

        Returns:
            A value list.
        '''
        aa_properties = pd.read_csv(aa_distribution_file)

        df_lookup = aa_properties.loc[:, ['1-letter code', lookup]]

        aa_lookup = {}
        
        for index, row in df_lookup.iterrows():

            aa = row['1-letter code']
            lookup_row= row[lookup]
            aa_lookup[aa] = float(lookup_row)
        
        ####

        seq = self.sequence

        seq_lookup = [aa_lookup[aa] for aa in seq]

        if len_sliding_window is not None:

            window = deque([], maxlen=len_sliding_window)
            seq_mean_lookup = []

            for pos, aa in enumerate(seq_lookup):
                window.append(aa)
                mean_window = sum(window)/len(window)
                seq_mean_lookup.append(mean_window)
        
            seq_lookup = seq_mean_lookup

        return seq_lookup
        

def plot_lookup(value_list, lookup = 'hydropathy index (Kyte-Doolittle method)'):
    '''Plots the lookup from the protein class.

    It uses plotly to plot the lookup.

    Args:
        value_list: a list with floats
        lookup: Specifies the lookup.
    Returns:
        A bar plot visualising the lookup.
    '''

    positions = range(1, (len(value_list)+1))

    df_plot = pd.DataFrame(
        {'Position': positions,
        lookup: value_list}
    )

    data = [
        go.Bar(
            x = df_plot['Position'],
            y = df_plot[lookup]

        )
    ]
    fig = go.Figure(data=data)
    fig.layout.title.text = f'{lookup} Lookup for {gprotein.name} with Sliding window 10'.upper()
    fig.layout.xaxis.title = f'Protein Sequence Position'
    fig.layout.yaxis.title = lookup
    fig.show()




#gprotein = ProteinClass(
#    name = "G-protein coupled receptor 183",
#    sequence = None,
#    protein_id = "P32249")

#gprotein.get_data()
#vl = gprotein.map(len_sliding_window= 10)
#plot_lookup(value_list = vl)
