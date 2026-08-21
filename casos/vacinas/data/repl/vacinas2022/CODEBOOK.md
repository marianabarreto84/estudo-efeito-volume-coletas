# Codebook do eixo B (v1) — gerado, nao editar a mao

> Extraido de `suplementar_rotulos.xlsx` por `pipeline/extrai_codebook.py`.
> Toda definicao vem do material suplementar do paper; os totais sao os
> publicados na Tabela 5 e foram conferidos contra a aba do gabarito.

## Stance

- `Tweet_ProVax` = 738 | `Tweet_AntiVax` = 784 | nenhum dos dois = 3 | total = 1525
- Sao mutuamente exclusivos no gabarito (0 tweets com ambos).

## Categorias amplas (14 — nao 11; ver nota)

> O corpo do preprint fala em 11 categorias; o suplemento numera **14**.
> Seguimos o suplemento, que e o dado.

| # | Categoria (paper) | PT-BR | Coluna do gabarito | Total | Pro | Anti |
|---|---|---|---|---:|---:|---:|
| 1 | Politics | Politica | `All_Category_1_Politics` | 719 | 356 | 363 |
| 2 | Children | Criancas | `About_all_Children` | 592 | 302 | 290 |
| 3 | Restrictive policies | Politicas restritivas | `All_Category_3_RestrictivePolicies` | 531 | 152 | 379 |
| 4 | Disadvantages of vaccines | Desvantagens das vacinas | `About_all_disadvantages_vaccines_` | 378 | 37 | 341 |
| 5 | Anti-vaccine people | Pessoas anti-vacina | `ALL_Category_5_AntivaxPeople` | 375 | 269 | 106 |
| 6 | International | Internacional | `About_Other_Countries` | 253 | 82 | 170 |
| 7 | Advantages of vaccines | Vantagens das vacinas | `About_all_advantages_vaccines` | 242 | 235 | 7 |
| 8 | COVID risks | Riscos da COVID | `About_COVID_risks` | 241 | 196 | 45 |
| 9 | Misinformation sources | Fontes de desinformacao | `About_Misinformation` | 201 | 141 | 60 |
| 10 | Information sources | Fontes de informacao | `About_All_InformationSources_Social_OR_Official` | 179 | 77 | 101 |
| 11 | Science | Ciencia | `About_SCIENCE` | 94 | 44 | 50 |
| 12 | Vaccines type or laboratories | Tipos de vacina / laboratorios | `About_All_VaccinesLabs_L1_to_L9_OR` | 86 | 19 | 67 |
| 13 | Religion | Religiao | `Religion` | 46 | 34 | 12 |
| 14 | Other drugs | Outras drogas | `About_OtherDrugs_CloroquinaORIvermectna` | 32 | 25 | 7 |

## Subcategorias (o que cada categoria abrange)

### 1. Politics (Politica)

- Government politicians — `About_Bolsonaro` (n=171, pro=119, anti=52)
- Government politicians — `About_GovernmentNotRegional` (n=74, pro=57, anti=17)
- Government politicians — `About_All_Bolsonaro_OR_GovNotRegional` (n=219, pro=154, anti=65)
- Pro-government politicians — `About_other_FarRight_politicians` (n=55, pro=39, anti=16)
- Other politicians — `About_senators_deputies_councilors` (n=131, pro=39, anti=92)
- Other politicians — `About_Regional_Governments` (n=17, pro=8, anti=9)
- Left-wing politicians — `About_Lula` (n=17, pro=9, anti=8)
- Left-wing politicians — `About_PT` (n=10, pro=2, anti=8)
- Left-wing politicians — `About_other_Left_politicians` (n=29, pro=5, anti=24)
- All left-wing politicians — `About_ALL_Left_politicians` (n=51, pro=13, anti=38)
- Opposition politicians — `Paes` (n=7, pro=1, anti=6)
- Opposition politicians — `Dória` (n=21, pro=3, anti=18)
- All politicians — `About_all_Brazilian_Politicians` (n=405, pro=213, anti=192)
- Anti-vacine policies — `About_Antivax_government` (n=250, pro=194, anti=56)
- Vaccination delay — `About_Vaccine_DELAY` (n=72, pro=68, anti=4)
- Public Consultation on COVID-19 child immunization — `About_public_consult` (n=35, pro=15, anti=20)
- All anti-vaccine policies — `About_All_AntiVaccine_policies` (n=297, pro=226, anti=71)
- Minister of National Health Services — `About_Queiroga` (n=58, pro=45, anti=13)
- Ministry of National Health Services — `About_MS` (n=54, pro=29, anti=25)
- Public National Health Services — `About_SUS` (n=33, pro=26, anti=7)
- National Health Surveillance Agency — `About_Anvisa` (n=105, pro=62, anti=43)
- All Public health government structures — `About_All_Public_health_gov_structures` (n=218, pro=140, anti=78)
- Corruption — `About_Corruption` (n=31, pro=23, anti=8)
- Lobby — `About_LOBBY` (n=47, pro=5, anti=42)
- All Political illegalities — `About_All_Corruption_OR_Lobby` (n=76, pro=27, anti=49)
- Political supporters — `About_Bolsonaro_Supporters` (n=85, pro=71, anti=14)
- Judiciary — `About_JUDICIARY` (n=154, pro=39, anti=115)
- _(fronteira)_ Antivax people and government — `About_All_Antivax_PeopleA1toA8_OR_Gov` (n=570)
- _(fronteira)_ International politicians — `Trump` (n=4)
- _(fronteira)_ International politicians — `Biden` (n=11)
- _(fronteira)_ International politicians — `About_Other_internationalPoliticians` (n=11)
- _(fronteira)_ All international politicians — `About_all_International_Politicians` (n=25)

### 2. Children (Criancas)

- Children — `About_All_Children` (n=592, pro=302, anti=290)
- Pro need of vaccine prescription for children — `PRO_prescript_for_kids` (n=6, pro=0, anti=6)
- Against need of vaccine prescription for children — `AGAINST_prescript_for_kids` (n=13, pro=13, anti=0)
- All vaccine prescription for children (pro and against) — `About_All_PrescriptionForKids_Pro_OR_Against` (n=284, pro=271, anti=13)
- _(fronteira)_ Pro-adult vaccination, but against childhood immunization against COVID-19 — `About_YesVAccine_BUT_NotForChildren_A8` (n=2)
- _(fronteira)_ Pro vaccine to school enrollment — `About_Pro_VaccineTo_SCHOOL_Enrollment` (n=9)
- _(fronteira)_ Against vaccine to school enrollment — `About_Against_VaccineTo_SCHOOL_Enrollment` (n=33)

### 3. Restrictive policies (Politicas restritivas)

- Pro freedom for the vaccinees — `Pro_ProVax_Freedom` (n=32, pro=31, anti=1)
- Against freedom for the anti-vaccine — `Against_Antivax_Freedom` (n=96, pro=96, anti=0)
- Pro mandatory vaccination — `Pro_Mandatory_vacc` (n=20, pro=20, anti=0)
- Pro vaccination but against its obligation — `About_YesVAccine_BUT_NotMandatory` (n=14, pro=1, anti=13)
- Pro freedom for the anti-vaccine — `Pro_AntiVax_Freedom` (n=335, pro=5, anti=330)
- Against mandatory vaccination — `Against_Mandatory_vacc` (n=167, pro=3, anti=164)
- Freedom — `About_All_FREEDOM_Pro_OR_Against_OR_Neutral` (n=439, pro=110, anti=329)
- Pro vaccine to university enrollment — `About_Pro_VaccineTo_UNIVERSITY_Enrollment` (n=4, pro=4, anti=0)
- Pro vaccine to school / University enrollment — `About_Pro_VaccineToSchoolORUniversityEnrollment` (n=12, pro=12, anti=0)
- Against vaccine to university enrollment — `About_Against_VaccineTo_UNIVERSITY_Enrollment` (n=12, pro=0, anti=12)
- Against vaccine to school / University enrollment — `About_Against_VaccineToSchoolORUniversityEnrollment` (n=41, pro=0, anti=41)
- School / University enrollment — `About_All_VaccineTo_SchoolORUniversity_Enrollment_ProORAgainst` (n=56, pro=13, anti=43)
- Pro COVID-19 vaccine certificate — `About_Pro_Vaccine_Passport_OR_Certificate` (n=89, pro=87, anti=2)
- Against COVID-19 vaccine certificate — `About_Against_Vaccine_Passport_OR_Certificate` (n=171, pro=1, anti=170)
- All COVID-19 vaccine certificate (pro and against) — `About_All_Vaccine_Passport_OR_Certificate_Pro_OR_Against` (n=260, pro=88, anti=172)
- _(fronteira)_ Pro vaccine to school enrollment — `About_Pro_VaccineTo_SCHOOL_Enrollment` (n=9)
- _(fronteira)_ Against vaccine to school enrollment — `About_Against_VaccineTo_SCHOOL_Enrollment` (n=33)

### 4. Disadvantages of vaccines (Desvantagens das vacinas)

- Non-severity of covid in children — `About_CHILD_NOT_risk` (n=31, pro=4, anti=27)
- Non-severity of covid — `About_omicron_NOT_risk` (n=25, pro=3, anti=22)
- Natural immunity is better than vaccine — `About_natural_immun` (n=21, pro=3, anti=18)
- Ineffectiveness of vaccines — `About_vacc_INEFFECTIVE` (n=152, pro=20, anti=132)
- Vaccine risks — `About_VACC_RISKS` (n=214, pro=8, anti=206)
- All disadvantages of vaccines — `About_all_disadvantages_vaccines_` (n=378, pro=37, anti=341)

### 5. Anti-vaccine people (Pessoas anti-vacina)

- Unvaccinated do not risk others — `About_Unvax_NOT_RiskOthers` (n=12, pro=0, anti=12)
- Unvaccinated risk others — `About_Unvax_RiskOthers` (n=36, pro=33, anti=3)
- All whether or not unvaccinated people are a risk to others — `About_All_Unvax_Risk_OR_Not_Others` (n=48, pro=33, anti=15)
- Anti- only COVID-19 vaccine — `About_AntiJustCOVIDvax_A1` (n=13, pro=1, anti=12)
- Oneself anti-vaccine — `About_Antivax_Oneself_A2` (n=3, pro=0, anti=3)
- General people anti-vaccine — `About_Antivax_GeneralPeople_Against_OR_Unvaxinated_A3` (n=189, pro=169, anti=20)
- Someone specific anti-vaccine — `About_Antivax_SomeoneSpecific_A4` (n=141, pro=112, anti=29)
- Pointing someone not vaccinated — `About_Antivax_SomeoneNOTvaccinated_A5` (n=25, pro=0, anti=25)
- Anti-vax movement — `About_Antivax_Movement_A6` (n=40, pro=20, anti=20)
- Anti-vaccination people who get vaccinated — `About_Antivax_Vaccinated_A7` (n=26, pro=23, anti=3)
- All mentions on anti-vaccination people — `About_All_AntivaxPeople_A1_OR_to_A8` (n=371, pro=269, anti=102)
- _(fronteira)_ Someone specific anti-vaccine / International — `Elon_Musk` (n=6)
- _(fronteira)_ Someone specific anti-vaccine / International — `Djokovic` (n=27)
- _(fronteira)_ Pro-adult vaccination, but against childhood immunization against COVID-19 — `About_YesVAccine_BUT_NotForChildren_A8` (n=2)
- _(fronteira)_ Antivax people and government — `About_All_Antivax_PeopleA1toA8_OR_Gov` (n=570)

### 6. International (Internacional)

- About countries other than Brazil — `USA` (n=58, pro=20, anti=38)
- About countries other than Brazil — `World` (n=32, pro=18, anti=14)
- About countries other than Brazil — `Australia` (n=25, pro=10, anti=15)
- About countries other than Brazil — `England_UK` (n=20, pro=4, anti=16)
- About countries other than Brazil — `Canada` (n=13, pro=4, anti=9)
- About countries other than Brazil — `Germany` (n=8, pro=0, anti=8)
- About countries other than Brazil — `Austria` (n=7, pro=0, anti=7)
- About countries other than Brazil — `France` (n=7, pro=2, anti=5)
- About countries other than Brazil — `Italy` (n=7, pro=3, anti=4)
- About countries other than Brazil — `Sweden` (n=7, pro=0, anti=7)
- About countries other than Brazil — `China` (n=5, pro=1, anti=4)
- About countries other than Brazil — `Europe` (n=5, pro=3, anti=2)
- About countries other than Brazil — `Israel` (n=5, pro=1, anti=4)
- About countries other than Brazil — `Mexico` (n=5, pro=1, anti=4)
- About countries other than Brazil — `Czech republic` (n=4, pro=1, anti=3)
- About countries other than Brazil — `Norway` (n=4, pro=0, anti=4)
- About countries other than Brazil — `South_Africa` (n=4, pro=1, anti=3)
- About countries other than Brazil — `Cuba` (n=3, pro=3, anti=0)
- About countries other than Brazil — `Argentina` (n=2, pro=1, anti=1)
- About countries other than Brazil — `Denmark` (n=2, pro=1, anti=1)
- About countries other than Brazil — `New_Zeland` (n=2, pro=0, anti=2)
- About countries other than Brazil — `Portugal` (n=2, pro=1, anti=0)
- About countries other than Brazil — `Serbia` (n=2, pro=0, anti=2)
- About countries other than Brazil — `South Korea` (n=2, pro=1, anti=1)
- About countries other than Brazil — `Spain` (n=2, pro=0, anti=2)
- About countries other than Brazil — `Switzerland` (n=2, pro=1, anti=1)
- About countries other than Brazil — `Belgium` (n=1, pro=0, anti=1)
- About countries other than Brazil — `Bolivia` (n=1, pro=0, anti=1)
- About countries other than Brazil — `Bulgaria` (n=1, pro=0, anti=1)
- About countries other than Brazil — `Georgia` (n=1, pro=0, anti=1)
- About countries other than Brazil — `Jamaica` (n=1, pro=1, anti=0)
- About countries other than Brazil — `Romania` (n=1, pro=0, anti=1)
- About countries other than Brazil — `Russia` (n=1, pro=0, anti=1)
- About countries other than Brazil — `Others_Indonesia_Turkmenistan_Tajikistan_NewCaledonia_and_Micronesia` (n=1, pro=0, anti=1)
- About countries other than Brazil — `About_Other_Countries` (n=253, pro=82, anti=170)
- _(fronteira)_ Someone specific anti-vaccine / International — `Elon_Musk` (n=6)
- _(fronteira)_ Someone specific anti-vaccine / International — `Djokovic` (n=27)
- _(fronteira)_ International politicians — `Trump` (n=4)
- _(fronteira)_ International politicians — `Biden` (n=11)
- _(fronteira)_ International politicians — `About_Other_internationalPoliticians` (n=11)
- _(fronteira)_ All international politicians — `About_all_International_Politicians` (n=25)

### 7. Advantages of vaccines (Vantagens das vacinas)

- Effectiveness of vaccines — `About_vacc_EFFECTIVE` (n=164, pro=157, anti=7)
- Vaccine safety — `About_Vacccine SAFE` (n=30, pro=30, anti=0)
- Misinformation on vaccine risks — `About_Misinf_Vacc_RISK` (n=71, pro=71, anti=0)
- All advantages of vaccines — `About_all_advantages_vaccines` (n=242, pro=235, anti=7)

### 8. COVID risks (Riscos da COVID)

- COVID risks — `About_COVID_risks` (n=241, pro=196, anti=45)

### 9. Misinformation sources (Fontes de desinformacao)

- Misinformation — `About_Misinformation` (n=201, pro=141, anti=60)

### 10. Information sources (Fontes de informacao)

- Social media — `About_Social_media` (n=63, pro=44, anti=18)
- Official media — `About_official_media` (n=118, pro=33, anti=85)
- All Information sources — `About_All_InformationSources_Social_OR_Official` (n=179, pro=77, anti=101)

### 11. Science (Ciencia)

- Science — `About_SCIENCE` (n=94, pro=44, anti=50)

### 12. Vaccines type or laboratories (Tipos de vacina / laboratorios)

- Vaccine labs — `About_VaccineLab_generally_L1` (n=12, pro=2, anti=10)
- Vaccine labs — `About_BioCuba_Pharma_L2` (n=1, pro=1, anti=0)
- Vaccine labs — `About_Moderna_L3` (n=1, pro=0, anti=1)
- Vaccine labs — `About_Butantan_L4` (n=5, pro=1, anti=4)
- Vaccine type / lab — `About_Sinovac_L5` (n=2, pro=0, anti=2)
- Vaccine type / lab — `About_Sputnik_L6` (n=2, pro=0, anti=2)
- Vaccine type / lab — `About_AstraZenecaOxford_L7` (n=8, pro=1, anti=7)
- Vaccine types — `About_CORONAVAC_L8` (n=11, pro=7, anti=4)
- Vaccine type / lab — `About_Pfizer_L9` (n=58, pro=12, anti=46)
- Vaccine labs — `About_CEO_Pfizer` (n=86, pro=19, anti=67)
- All vaccine types or labs — `About_All_VaccinesLabs_L1_to_L9_OR` (n=7, pro=0, anti=7)

### 13. Religion (Religiao)

- Religion — `Religion` (n=46, pro=34, anti=12)

### 14. Other drugs (Outras drogas)

- Other drugs disproved against COVID — `About_OtherDrugs_CloroquinaORIvermectna` (n=32, pro=25, anti=7)
