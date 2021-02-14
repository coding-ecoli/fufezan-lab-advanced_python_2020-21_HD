import pytest
import sys, os
sys.path.insert(1, '/Users/huuumath/Git/fufezan-lab-advanced_python_2020-21_HD/homeworks/e04')

from protein_class import ProteinClass

def test_protein_class():
    protein = ProteinClass(
        name = "helloprotein",
        sequence = 'FA',
        protein_id = 'helloxyz1')
    assert protein.sequence == 'FA'
    assert protein.name == 'helloprotein'
    assert protein.protein_id == 'helloxyz1'

def test_protein_class2():
    protein = ProteinClass(
        name = 'G-protein',
        sequence = None,
        protein_id = 'P32249'
    )
    assert protein.sequence is None

def test_protein_class3():
    protein = ProteinClass(
        name = 'G-protein',
        sequence = None,
        protein_id = 'P32249' 
    )
    protein.get_data()
    assert protein.sequence == 'MDIQMANNFTPPSATPQGNDCDLYAHHSTARIVMPLHYSLVFIIGLVGNLLALVVIVQNRKKINSTTLYSTNLVISDILFTTALPTRIAYYAMGFDWRIGDALCRITALVFYINTYAGVNFMTCLSIDRFIAVVHPLRYNKIKRIEHAKGVCIFVWILVFAQTLPLLINPMSKQEAERITCMEYPNFEETKSLPWILLGACFIGYVLPLIIILICYSQICCKLFRTAKQNPLTEKSGVNKKALNTIILIIVVFVLCFTPYHVAIIQHMIKKLRFSNFLECSQRHSFQISLHFTVCLMNFNCCMDPFIYFFACKGYKRKVMRMLKRQVSVSISSAVKSAPEENSREMTETQMMIHSKSSNGK'
    
def test_protein_class4():
    protein = ProteinClass(
        name = 'G-protein',
        sequence= '2345',
        protein_id = 'P32249'
    )
    protein.get_data()
    assert protein.sequence == 'MDIQMANNFTPPSATPQGNDCDLYAHHSTARIVMPLHYSLVFIIGLVGNLLALVVIVQNRKKINSTTLYSTNLVISDILFTTALPTRIAYYAMGFDWRIGDALCRITALVFYINTYAGVNFMTCLSIDRFIAVVHPLRYNKIKRIEHAKGVCIFVWILVFAQTLPLLINPMSKQEAERITCMEYPNFEETKSLPWILLGACFIGYVLPLIIILICYSQICCKLFRTAKQNPLTEKSGVNKKALNTIILIIVVFVLCFTPYHVAIIQHMIKKLRFSNFLECSQRHSFQISLHFTVCLMNFNCCMDPFIYFFACKGYKRKVMRMLKRQVSVSISSAVKSAPEENSREMTETQMMIHSKSSNGK'

def test_protein_class5():
    protein = ProteinClass(
        name = 'Somatostatin',
        sequence = 'AGCKNFFWKTFTSC',
        protein_id = 'unknown'
    )
    hydropathy_list = protein.map()
    assert hydropathy_list == [1.8, -0.4, 2.5, -3.9, -3.5, 2.8, 2.8, -0.9, -3.9, -0.7, 2.8, -0.7, -0.8, 2.5]

def test_protein_class6():
    protein = ProteinClass(
        name = 'Somatostatin',
        sequence = 'AGCKNFFWKTFTSC',
        protein_id = 'unknown'
    )
    hydropathy_list = protein.map(len_sliding_window = 2)
    assert hydropathy_list == [1.8, 0.7, 1.05, -0.7, -3.7, -0.3500000000000001, 2.8, 0.95, -2.4, -2.3, 1.0499999999999998, 1.0499999999999998, -0.75, 0.85]