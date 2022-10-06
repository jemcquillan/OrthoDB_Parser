import gzip
import argparse

level_of_interest = "4751" #fungi?
#scientific_names_of_interest = {"Talaromyces marneffei ATCC 18224", "[Candida] glabrata", "Candida dubliniensis CD36", "Cryptococcus neoformans var. neoformans JEC21", "Schizophyllum commune H4-8", "Colletotrichum graminicola M1.001", "Coccidioides immitis RS", "Fusarium verticillioides 7600", "Schizosaccharomyces octosporus yFS286", "Paracoccidioides lutzii Pb01", "Trichoderma atroviride IMI 206040", "Spizellomyces punctatus DAOM BR117", "Sordaria macrospora k-hell", "Coprinopsis cinerea okayama7#130", "Batrachochytrium dendrobatidis JAM81", "Melampsora larici-populina 98AG31", "Chaetomium thermophilum var. thermophilum DSM 1495", "Yamadazyma tenuis ATCC 10573", "Leptosphaeria maculans JN3", "Stereum hirsutum FP-91666 SS1", "Punctularia strigosozonata HHB-11173 SS5", "Fomitiporia mediterranea MF3/22", "Coniophora puteana RWD-64-598 SS2", "Tremella mesenterica DSM 1558", "Dichomitus squalens LYAD-421 SS1", "Coniosporium apollinis CBS 100218", "Phanerochaete carnosa HHB-10118-sp", "Fibroporia radiculosa", "Heterobasidion irregulare TC 32-1", "Ustilago maydis 521", "Gloeophyllum trabeum ATCC 11539", "Bipolaris maydis ATCC 48331", "Wallemia ichthyophaga EXF-994", "Glarea lozoyensis ATCC 20868", "Kalmanozyma brasiliensis GHG001", "Kwoniella pini CBS 10737", "Pestalotiopsis fici W106-1", "Kuraishia capsulata CBS 1993", "Exophiala aquamarina CBS 119918", "Fonsecaea pedrosoi CBS 271.37", "Rhinocladiella mackenziei CBS 650.93", "Verruconis gallopava", "Lachancea lanzarotensis", "Cutaneotrichosporon oleaginosum", "Malassezia pachydermatis", "Rhodotorula graminis WP1", "Pneumocystis jirovecii RU7", "Xylona heveae TC161", "Cordyceps fumosorosea ARSEF 2679", "Pichia membranifaciens NRRL Y-2026", "Babjeviella inositovora NRRL Y-12698", "Ascoidea rubescens DSM 1968", "Cyberlindnera jadinii NRRL Y-1542", "Metschnikowia bicuspidata var. bicuspidata NRRL YB-4993", "Diplodia corticola", "Penicilliopsis zonata CBS 506.65", "Kockovaella imperatae", "Lobosporangium transversale", "Postia placenta MAD-698-R-SB12", "Aspergillus novofumigatus IBT 16806", "Phycomyces blakesleeanus NRRL 1555(-)"}
Ortho_DB_org_ids_of_interest = {"441960_1", "5478_1", "573826_1", "214684_1", "578458_1", "645133_1", "246410_1", "334819_1", "483514_1", "502779_1", "452589_1", "645134_1", "771870_1", "240176_1", "684364_1", "747676_1", "759272_1", "590646_1", "985895_1", "721885_1", "741275_1", "694068_1", "741705_1", "578456_1", "732165_1", "1168221_1", "650164_1", "599839_1", "747525_1", "237631_1", "670483_1", "665024_1", "1299270_1", "1116229_1", "1365824_1", "1296096_1", "1229662_1", "1382522_1", "1182545_1", "1442368_1", "1442369_1", "253628_1", "1245769_1", "879819_1", "77020_1", "578459_1", "1408657_1", "1328760_1", "1081104_1", "763406_1", "984486_1", "1344418_1", "983966_1", "869754_1", "236234_1", "1073090_1", "4999_1", "64571_1", "670580_1", "1392255_1", "763407_1"}
# ^These IDs come from OrthoDB advanced search tree search for the organisms of interest.

OG_unique_ids = set() #Open set to build the OG unique id's

'''
This creates a file (fungi_genes_in_orgs_of_interest.txt) with all the unique genes of
interest for each organism we want, output file *_genes_in_orgs_of_interest.txt.
'''
with gzip.open("/Volumes/GoogleDrive/My Drive/OrthoDB/OrthoDB_data/odb10v1_OG2genes.tab.gz", "rt") as OG2genes_file, open("/Volumes/GoogleDrive/My Drive/OrthoDB/fungi_complexity_orthologs/Fungi_OrthoDB_Gene_Parse_Output/fungi_genes_in_orgs_of_interest.txt", "w") as gene_file:
	for line in OG2genes_file:
		OG_unique_id, Ortho_DB_gene_id = line.strip().split("\t")
		org_id = Ortho_DB_gene_id.split(":")[0]
		if (OG_unique_id.endswith("at"+level_of_interest)) and (org_id in Ortho_DB_org_ids_of_interest):
			OG_unique_ids.add(OG_unique_id)
			gene_file.write(f"{Ortho_DB_gene_id}\n")# formatted string, let you put variable in the braces and turns them into a string. The Braces are notation for a variable object.

'''
This creates a file (fungi_OGs.txt) with all the unique OG cluster IDs, output file *_OGs.txt.
'''
with open("/Volumes/GoogleDrive/My Drive/OrthoDB/fungi_complexity_orthologs/Fungi_OrthoDB_Gene_Parse_Output/fungi_OGs.txt", "w") as OG_file:
	for OG_unique_ids in OG_unique_ids:
		OG_file.write(f"{OG_unique_id}\n")

'''
Since it takes so long to build the fungi_genes_in_orgs_of_interest.txt, we load it in 
after is has been created so we don't have to wait for it to build and have it stored in *
memory.
'''
fungi_genes_in_orgs_of_interest = set()
with open("/Volumes/GoogleDrive/My Drive/OrthoDB/fungi_complexity_orthologs/Fungi_OrthoDB_Gene_Parse_Output/fungi_genes_in_orgs_of_interest.txt", "r") as genes_file:
	for line in genes_file:
		Ortho_DB_gene_id = line.strip()
		fungi_genes_in_orgs_of_interest.add(Ortho_DB_gene_id)

'''
Makes the output file to have the whole line found from the species:gene's of interest
from the odb10v1_gene_xrefs.tab.gz file, output file output.ncbigid.txt.
'''
with gzip.open("/Volumes/GoogleDrive/My Drive/OrthoDB/OrthoDB_data/odb10v1_gene_xrefs.tab.gz", "rt") as gene_xrefs_file, open("/Volumes/GoogleDrive/My Drive/OrthoDB/fungi_complexity_orthologs/Fungi_OrthoDB_Gene_Parse_Output/output.ncbigid.txt", "w") as output_file:
	for line in gene_xrefs_file:
		Ortho_DB_gene_id, ext_gene_id, ext_db = line.strip().split("\t")
		if Ortho_DB_gene_id in fungi_genes_in_orgs_of_interest and ext_db == "NCBIgid":
			output_file.write(line)