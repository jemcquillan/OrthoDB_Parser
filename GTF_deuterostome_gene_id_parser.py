import gzip
import sys
import re

Ortho_DB_org_ids_of_interest = {"9606_0", "10090_0", "9785_0", "7955_0", "7668_0", "9615_0", "13616_0", "9823_0", "9986_0", "7739_0", "8364_0", "28377_0", "10141_0", "30608_0", "9685_0", "176946_0", "7719_0", "7897_0", "13735_0", "8496_0", "9365_0", "9371_0", "9733_0", "246437_0", "8932_0", "38654_0", "8081_0", "482537_0", "94827_0", "128390_0", "125878_0", "336983_0", "9568_0", "379532_0", "202946_0", "35019_0", "146911_0", "9157_0", "7741_0", "259920_0", "8502_0", "94835_0", "8128_0", "133434_0", "8090_0", "9913_0", "9749_0", "9796_0", "9598_0", "9601_0", "1415176_0", "9544_0", "59729_0", "9258_0", "61853_0", "9595_0", "9483_0", "8078_0", "9739_0", "9978_0", "10116_0", "8469_0", "8839_0", "9031_0", "7868_0", "103695_0", "31033_0", "9305_0"}
#Set of all the orthoDB species ID's
org_id_to_gtf = {"9606_0":"GCF_000001405.39_GRCh38.p13_genomic.gtf.gz", "10090_0":"GCF_000001635.27_GRCm39_genomic.gtf.gz", "9785_0":"GCF_000001905.1_Loxafr3.0_genomic.gtf.gz", "7955_0":"GCF_000002035.6_GRCz11_genomic.gtf.gz", "7668_0":"GCF_000002235.5_Spur_5.0_genomic.gtf.gz", "9615_0":"GCF_000002285.3_CanFam3.1_genomic.gtf.gz", "13616_0":"GCF_000002295.2_MonDom5_genomic.gtf.gz", "9823_0":"GCF_000003025.6_Sscrofa11.1_genomic.gtf.gz", "9986_0":"GCF_000003625.3_OryCun2.0_genomic.gtf.gz", "7739_0":"GCF_000003815.1_Version_2_genomic.gtf.gz", "8364_0":"GCF_000004195.4_UCB_Xtro_10.0_genomic.gtf.gz", "28377_0":"GCF_000090745.1_AnoCar2.0_genomic.gtf.gz", "10141_0":"GCF_000151735.1_Cavpor3.0_genomic.gtf.gz", "30608_0":"GCF_000165445.2_Mmur_3.0_genomic.gtf.gz", "9685_0":"GCF_000181335.3_Felis_catus_9.0_genomic.gtf.gz", "176946_0":"GCF_000186305.1_Python_molurus_bivittatus-5.0.2_genomic.gtf.gz", "7719_0":"GCF_000224145.3_KH_genomic.gtf.gz", "7897_0":"GCF_000225785.1_LatCha1_genomic.gtf.gz", "13735_0":"GCF_000230535.1_PelSin_1.0_genomic.gtf.gz", "8496_0":"GCF_000281125.3_ASM28112v4_genomic.gtf.gz", "9365_0":"GCF_000296755.1_EriEur2.0_genomic.gtf.gz", "9371_0":"GCF_000313985.2_ASM31398v2_genomic.gtf.gz", "9733_0":"GCF_000331955.2_Oorc_1.1_genomic.gtf.gz", "246437_0":"GCF_000334495.1_TupChi_1.0_genomic.gtf.gz", "8932_0":"GCF_000337935.1_Cliv_1.0_genomic.gtf.gz", "38654_0":"GCF_000455745.1_ASM45574v1_genomic.gtf.gz", "8081_0":"GCF_000633615.1_Guppy_female_1.0_MT_genomic.gtf.gz", "482537_0":"GCF_000696425.1_G_variegatus-3.0.2_genomic.gtf.gz", "94827_0":"GCF_000705375.1_ASM70537v2_genomic.gtf.gz", "128390_0":"GCF_000708225.1_ASM70822v1_genomic.gtf.gz", "125878_0":"GCF_000935625.1_ASM93562v1_genomic.gtf.gz", "336983_0":"GCF_000951035.1_Cang.pa_1.0_genomic.gtf.gz", "9568_0":"GCF_000951045.1_Mleu.le_1.0_genomic.gtf.gz", "379532_0":"GCF_000956105.1_Pcoq_1.0_genomic.gtf.gz", "202946_0":"GCF_001039765.1_AptMant0_genomic.gtf.gz", "35019_0":"GCF_001077635.1_Thamnophis_sirtalis-6.0_genomic.gtf.gz", "146911_0":"GCF_001447785.1_Gekko_japonicus_V1.1_genomic.gtf.gz", "9157_0":"GCF_001522545.3_Parus_major1.1_genomic.gtf.gz", "7741_0":"GCF_001625305.1_Haploidv18h27_genomic.gtf.gz", "259920_0":"GCF_001642345.1_ASM164234v2_genomic.gtf.gz", "8502_0":"GCF_001723895.1_CroPor_comp1_genomic.gtf.gz", "94835_0":"GCF_001723915.1_GavGan_comp1_genomic.gtf.gz", "8128_0":"GCF_001858045.2_O_niloticus_UMD_NMBU_genomic.gtf.gz", "133434_0":"GCF_001949145.1_OKI-Apl_1.0_genomic.gtf.gz", "8090_0":"GCF_002234675.1_ASM223467v1_genomic.gtf.gz", "9913_0":"GCF_002263795.1_ARS-UCD1.2_genomic.gtf.gz", "9749_0":"GCF_002288925.2_ASM228892v3_genomic.gtf.gz", "9796_0":"GCF_002863925.1_EquCab3.0_genomic.gtf.gz", "9598_0":"GCF_002880755.1_Clint_PTRv2_genomic.gtf.gz", "9601_0":"GCF_002880775.1_Susie_PABv2_genomic.gtf.gz", "1415176_0":"GCF_002925995.2_T_m_triunguis-2.0_genomic.gtf.gz", "9544_0":"GCF_003339765.1_Mmul_10_genomic.gtf.gz", "59729_0":"GCF_003957565.2_bTaeGut1.4.pri_genomic.gtf.gz", "9258_0":"GCF_004115215.2_mOrnAna1.pri.v4_genomic.gtf.gz", "61853_0":"GCF_006542625.1_Asia_NLE_v1_genomic.gtf.gz", "9595_0":"GCF_008122165.1_Kamilah_GGO_v0_genomic.gtf.gz", "9483_0":"GCF_009663435.1_Callithrix_jacchus_cj1700_1.1_genomic.gtf.gz", "8078_0":"GCF_011125445.2_MU-UCD_Fhet_4.1_genomic.gtf.gz", "9739_0":"GCF_011762595.1_mTurTru1.mat.Y_genomic.gtf.gz", "9978_0":"GCF_014633375.1_OchPri4.0_genomic.gtf.gz", "10116_0":"GCF_015227675.2_mRatBN7.2_genomic.gtf.gz", "8469_0":"GCF_015237465.2_rCheMyd1.pri.v2_genomic.gtf.gz", "8839_0":"GCF_015476345.1_ZJU1.0_genomic.gtf.gz", "9031_0":"GCF_016699485.2_bGalGal1.mat.broiler.GRCg7b_genomic.gtf.gz", "7868_0":"GCF_018977255.1_IMCB_Cmil_1.0_genomic.gtf.gz", "103695_0":"GCF_900067755.1_pvi1.1_genomic.gtf.gz", "31033_0":"GCF_901000725.2_fTakRub1.2_genomic.gtf.gz", "9305_0":"GCF_902635505.1_mSarHar1.11_genomic.gtf.gz"}
#Dictionary of keys being OrthoDB species ID's: values being the GTF file names

for OG_Species in Ortho_DB_org_ids_of_interest:
	GTF = org_id_to_gtf[OG_Species]
	with open('/Volumes/GoogleDrive/My Drive/OrthoDB/deuterostome_complexity_orthologs/Deuterostome_OrthoDB_Gene_Parse_Output/deuterostome_output.ncbigid.txt', 'r') as OrthoDB_ncbigid, gzip.open("/Volumes/GoogleDrive/My Drive/OrthoDB/deuterostome_complexity_orthologs/Deuterostome_Whole_Genome_GTFs/"+GTF, "rt") as Species_GTF:
		GeneID_xrefs_GTF = set()
		for line in OrthoDB_ncbigid:
			OG_unique_geneid, NCBIgid, ext_DB = line.strip().split()
			OG_SpeciesID = OG_unique_geneid.split(':')[0]
			if OG_SpeciesID == OG_Species:
				GeneID_xrefs_GTF.add(NCBIgid)
	#	print(GeneID_xrefs_GTF.pop())
		Species_GeneIDs = set()
		for line in Species_GTF:
			if not line.startswith('#'):
				GTF_feature = line.split('\t')[2]
				if GTF_feature == "gene":
					GTF_attr = line.split('\t')[8]
	#				print(GTF_attr)
					for GeneID in GTF_attr.split(";"):
						if ' db_xref "GeneID:' in GeneID:
	#						print(GeneID)
							xref = GeneID[17:-1]
	#				print(xref)
					if xref in GeneID_xrefs_GTF:
						gene_id = GTF_attr.split(";")[0]
	#					print(gene_id)
						Species_GeneIDs.add(gene_id)
		
	with gzip.open("/Volumes/GoogleDrive/My Drive/OrthoDB/deuterostome_complexity_orthologs/Deuterostome_Whole_Genome_GTFs/"+GTF, "rt") as Species_GTF, gzip.open("/Volumes/GoogleDrive/My Drive/OrthoDB/deuterostome_complexity_orthologs/Deuterostome_filtered_GTFs/"+GTF[:-7]+".OG_filter.gtf.gz", "wb") as OG_Species, gzip.open("/Volumes/GoogleDrive/My Drive/OrthoDB/deuterostome_complexity_orthologs/Deuterostome_novel_gene_GTFs/"+GTF[:-7]+".novel.gtf.gz", "wb") as Novel_Species:
		for line in Species_GTF:
			if not line.startswith('#'):
				gene_id = line.split('\t')[8].split(";")[0]
				if gene_id in Species_GeneIDs:
					OG_Species.write(line.encode('utf-8'))
				else:
					Novel_Species.write(line.encode('utf-8'))

