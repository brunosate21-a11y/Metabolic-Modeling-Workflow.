# Changelog

## 1.0.0 (2026-06-16)


### Features

* Add meta.yaml in bio ([2fdf411](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/2fdf4119883e65d593eabad934fb519855bb9e8d))
* Add rules.smk and delete the "wrapper" part inside and add the "conda", "script" part with the right paths ([65d8758](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/65d8758724ec7bde9a45beed168c9da4b4bea6fa))
* Adicionar a rule filter_memote ([5845beb](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/5845beb4e070d777177c708b0bac153ac8e82879))
* Changing the channels order on the workflow env ([358418e](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/358418eacd80cd2978280ea97e08e0417f769a50))
* **checkm:** make pipeline portable with auto-download of DB ([5ecbfe3](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/5ecbfe3957bac745c044b0b2cbcb3e11d16daeaa))
* Creação de um script produzido pelo memote, que extrai o score total e as métricas chave e por fim escreve tudo num só unico TSV ([812d2e9](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/812d2e9b441f20237b42a680654a5bbe587052f0))
* criar uma lista de genomas para procurar ([9523d02](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/9523d02a8f4600ab19bcd5db160063d1c08529d1))
* deleted common rule ([2b4ddda](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/2b4ddda6af0b3ae8cb9e8ac0cf8c82eb3495e301))
* deletes rule ([c631682](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/c631682bfb17241c2d36df8ae0b9cbec94af20bd))
* Leitura dos ficheiros score.json do memote e filtra por score total ([8892ff2](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/8892ff2e0766b7035d34811e61f1041f5f96505e))
* micom name changed ([41e6789](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/41e67892bc298591ae57343eac81aabb4a94ef39))
* micom.smk fix name ([8f98c6c](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/8f98c6c2a12f3d7365d61a9829f90009f78a9368))
* miniupdate ([253b001](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/253b001044b4751d0dc987315f11662887bc4d2e))
* Moving .yaml from bio to workflow/env ([e495be9](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/e495be9ea16bf39f610bb7a7dc957c68ef40a0f8))
* Moving the envirnoment of the wrappers to the right place ([3033cde](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/3033cdee72d8c661502a7a8a61f22a19c7e766a4))
* Moving the wrappers to the script fold ([3772046](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/3772046f420ef1ca830ec8ebb12fe60ac235e52a))
* Not necessary ([cf138f0](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/cf138f080054f97a66450e2b863c1e862112db39))
* novos dados ([86c3a36](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/86c3a361dd3e7a377cdda1a696ee852ff2917730))
* pipeline completo com CPLEX e autodetect de MAGs ([22d27db](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/22d27db8b51d4e956ff73424d7fec2b4a605397b))
* recebe ficheiros quality.tsv do CheckM, aplica thresholds do config e produz 2 outputs: uma tabela resumo com pass/fail e uma lista dos MAGs que passam ([2a4b4f1](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/2a4b4f11a697e2b7a62fd98e9c29573c01d58afc))
* Steup do sensitivity ([8916713](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/8916713e66e3da701db5b9e5039a8610d1f2f8a2))
* test micom and steadycom ([b79b91f](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/b79b91ffbb686bd3b824cd6b93b338e86e9dca63))
* update da workflow snakefile. Rever antes de entregar no final para o fna ([af81dcf](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/af81dcfa6ef07fb2bfe018b9530ae4e90d242ed6))


### Bug Fixes

* 3 methods comparison ([d2ebd95](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/d2ebd953058ce11df7e2bece1b426942a958864d))
* add include memote and outputs of memote in rule all ([05f2ca3](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/05f2ca3ef38a5c2bb4338be927502ac9d2e915bd))
* adicionar thresholds de qualidade. Seguem o minimo razoavel para modelos metabolicos (completude &gt;=50 e contaminação &lt; = 10) - Podemos ter que alterar isto ([7cba2d7](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/7cba2d7243a8988ad3dbf025444056aa462f5420))
* autodetect MAGs + download script ([46a40ae](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/46a40ae000ef32e4d933c4ea5a887ecc10752435))
* Correção do path relativo e adição de um local para filtragem downstream ([ea8ade6](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/ea8ade6c5a5183fec47958ef0dcfd0d10a1788cf))
* correção dos paths e adicionar a rule do filter_checkM ([a19d38c](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/a19d38c8e88af517b3b8cac94711d274e04658a1))
* correct workflow paths and carveme arguments ([37b486e](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/37b486e812f639e06175df75939cf3899a0b1391))
* Corrects output names — SMETANA uses -o as a prefix, not as a filename. It passes a generic prefix and renames to the names expected by Snakemake. ([e33de8a](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/e33de8a8fdd95f496a67d4e087099e8463df0355))
* corrigir caminhos e argumentos do workflow ([35ea1c4](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/35ea1c4a22c3c8358861189a892cd32b55bd85c5))
* Dependencies correction ([e53eeac](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/e53eeacd072735c54b2d26f49329f48c4da4e931))
* desnecessário e limpeza estética ([f1c86f3](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/f1c86f3c4e5e00bbb70b9de4f1ab101bd05b7441))
* Envs do template, não necessário ([98e8a75](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/98e8a75a7b8b84030e2a7c6b020e360e4c4e1ebe))
* fillter workinggg!! ([21c91e2](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/21c91e273f2666944102db3cac8409ce74f494d8))
* fix ([a46a8ea](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/a46a8eaf5882a3afb1474049901e1bedac99218c))
* fix ([2423205](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/24232059022346b696d1785fb301892cff2d8690))
* fix dependencies ([fe7ddf9](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/fe7ddf9f4bd17f25a09344887c746119f860dfc1))
* fix filter checkm ([eace0e3](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/eace0e38aef44f7ff5439feb7508bce834008ead))
* implement MICOM and SteadyCom wrappers, fix SMETANA flags ([6dde237](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/6dde2379e021dbcc5dc950e7020b975c484dcff4))
* memote filter working ([65cd0e6](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/65cd0e6d2e6aa4c9ec3173cc716d73404208b730))
* new fix ([ee085dd](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/ee085dddd1e4d16432c96b47514f3dceb8289092))
* new genomes ([d197718](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/d197718f24bf6d1bee04f0221c3e7b6a174036e2))
* new results on snakefile ([165c612](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/165c6123d217283e5cdf5c581ed99f5a094c8b6a))
* preparar para vários faa ([825d949](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/825d9499ac001873211d7a0e3a5c250a409caa54))
* reduce tree ([3e492c5](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/3e492c5a296c13d691a00e8dba074a20c82391eb))
* remover os passos ([a6e4d5f](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/a6e4d5ffa4fc605753b67b2748f2bba8f0ace23d))
* rule:checkm - inout faa insted of fna ([88e6749](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/88e6749802d14b3aa9ae59cada59f517ca95c346))
* são apenas documentação descritiva, o snakemake nao usa estes ficheiros, não faz falta ([2716e69](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/2716e694897d3fb9bba1545f1baba4ad84b92924))
* schemas validam parametros do template original que nao fazem parte deste workflow ([4b67bef](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/4b67bef9c85ac1e97bbf0bf6eeac283fedbc0d75))
* script validação do template, não faz falta ([cd1ae88](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/cd1ae8878dabd484492638795867dc565a46c3b8))
* snakefile fixed ([1895e3f](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/1895e3fef8b657b0894ca8f0bd44ec7645a33b8b))
* solver change to scip ([c3cd989](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/c3cd989ef95e660aa3cd77d0f80a073dce947430))
* trocar de solver ([7ecaa9e](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/7ecaa9e965397afdcf05cd94bad5674611ba14ba))
* trocar de solver no config ([d502c9b](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/d502c9b39c60a092a173b9d4bc891bdb45069e3a))
* update checkm.py ([16cfa3b](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/16cfa3bfa93cdbfabfe565b8f476c1a8caf72386))
* update readme ([e0562fc](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/e0562fc4268703d0e39155ccc6810d13d2b09c26))
* work-env.checkm.yamla adicionar python 3.10 e setuptools ([ebc0076](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/ebc00760bb132455f624c483198dbd422d15df94))
* workflow fix ([98a4099](https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow./commit/98a4099372b76bb676149ff98cbf637352b9bac0))

## [1.3.0](https://github.com/snakemake-workflows/snakemake-workflow-template/compare/v1.2.0...v1.3.0) (2026-03-27)


### Features

* various changes to accomodate new wf catalog features ([7842e34](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/7842e34fccfe36e9aae766e6ce1892f6ee2c6155))


### Bug Fixes

* license year, new rules ordering with snakefmt, wrapper updates ([20958fb](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/20958fbf218257e68207c18ba28798ba6a9cd5ce))
* update github CI workflows ([5835ce7](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/5835ce7580e7c8a0b98f46f27d41094c692d9677))
* updated schema so all wf params are rendered in catalog ([dbadc80](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/dbadc80556dbc69cca53fd576067efe6a52ec89c))

## [1.2.0](https://github.com/snakemake-workflows/snakemake-workflow-template/compare/v1.1.0...v1.2.0) (2026-01-20)


### Features

* add profile info ([a42db58](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/a42db586610df85a78995c1fc9503553b2fab1ce))
* added profiles directory with a README.txt ([d0a8ea2](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/d0a8ea26f321fb8d3b2f0825e4a34b3d8c92948a))
* included information to the profiles directory ([a1b6b49](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/a1b6b495aaeb340a990f52a2d4d3e5440e2f6a67))


### Bug Fixes

* added missing content section ([014867f](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/014867f449ec6c00cad16850a827ef0df026eb50))
* move schemas folder from `config/` to `workflow/` ([605c11e](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/605c11e447b1de66eb9284e8df18a66f4273f079))
* move schemas folder from `config/` to `workflow/` ([a0d2f03](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/a0d2f03ac2888f77248f00068dbdd46c028d747a))
* switch from `samplesheet` to `sample_sheet`, as this is not a compound word ([8da47d7](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/8da47d771a48159ee05480ccb73937faf0a02279))
* switch from `samplesheet` to `sample_sheet`, as this is not a compound word ([d7e4ab3](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/d7e4ab351b3513a182847bf76bacc1addfa90641))

## [1.1.0](https://github.com/snakemake-workflows/snakemake-workflow-template/compare/v1.0.0...v1.1.0) (2025-07-29)


### Features

* complete minimal workflow as template ([2348055](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/234805535a6353a3db59d5bba0a4b38fe8194d97))
* complete, reproducible example workflow ([1dfa7ad](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/1dfa7adb0120880ae5e85c57551d5e698a057497))
* larger update to feature fully-functional example and github actions ([93c08fc](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/93c08fc9db2f8619af7b90784db83d18ed656f25))
* major simplification of rules, replacement of others by wrappers ([3811ef7](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/3811ef796df4fe38fb7161f9a1b06fac9db86d5b))
* major simplification of template and update docs ([81ee089](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/81ee08989857366893593a333615523f05295f87))
* replaced get genome script with simple shell command ([9208995](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/9208995b78433ce3680a0b0e453ddcf5915abcef))
* update github actions workflow in linting part ([27d53ee](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/27d53eecfad935f50bc62a30248141891a4329ee))
* update github actions workflow. check formatting of yaml files using prettier ([9f5131b](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/9f5131bf0eeaf1eb7fb0937b2840f73db2a02724))
* updated all GH actions to latest versions ([4d7b3a2](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/4d7b3a2b143c304b6dcf487664c392c4a5e98f74))
* updated github actions workflow ([fd36648](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/fd3664841b830ae670549aabb214eb6004aa696d))
* updated github actions workflow ([7a3a40e](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/7a3a40e62df01b37a802a085e7210014eb3fba82))


### Bug Fixes

* 2nd attempt to fix release please wf ([f81847f](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/f81847fdfd39d99e795006da4f84701ee6ba8ddc))
* added usage docs ([776b97e](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/776b97e3d0e928d98f4c48e619090b47f702dcab))
* all-temp needs explicit input of multiqc zip dirs ([026c35a](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/026c35aebfb140746bc823ce06327e25c9a40cf1))
* change release type to 'go', fixes release please wf ([658c784](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/658c784ab5d70b117ce9dd386f5b07f8e4ff782d))
* change release type to 'go', fixes release please wf ([a81ab9d](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/a81ab9def05667e23c5e59ac881c7a57b9f1b767))
* code review issues ([97faf1a](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/97faf1ae8bde189094e6b46568f3911f01b625fd))
* dont remove temp files for test runs ([0c2c8d1](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/0c2c8d19c51648872d09a8f697826b9445bafc81))
* formatting, logging ([d6c819e](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/d6c819efcadde1ad4af342152d3aef2a982983d0))
* lint error and docs update ([cf59f11](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/cf59f11acc11c01866ad56971fd132661f4f32be))
* recommended `.yaml` file extension, latest schema version ([e649e12](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/e649e12be9c447e8c366847ddf3531e216306c97))
* release please workflow requires additional permission ([0993271](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/0993271f0077e5a548755679b2b8952d18795580))
* release please workflow requires additional permission ([3651295](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/36512953f851611f18676a4f18e6e5684932ef61))
* removed unused templates, update catalog yml ([b5c292f](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/b5c292ff4b476441d8068ca8013e3b931d30fc04))
* revert to GitHub Actions status badge requiring `owner` and `repo` set by user ([dd163f3](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/dd163f33a5299ecbeb10eb019ef5e8c727f0422a))
* snakefmt error ([70d670a](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/70d670a91c79c0a9d89c59fff6add3f1036753a3))
* update release-please GH workflow ([1dad25d](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/1dad25da5de222982b0cdf35a91be6ecc5a81a42))
* update release-please GH workflow ([0ea4df2](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/0ea4df2f746e0fc760c06a3b902e2ee8bdf2ff42))
* update snakemake action ([fac8662](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/fac8662193fa501fdfc2f3bb94e7549b96dec500))
* updated schemas and params docs ([facf377](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/facf377a7cc107b3e8db0793b21027a9f3df0eeb))
* updates to enable release-please action again ([8d9552b](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/8d9552b8369ca6b115ee00777f45cf641312dde3))
* use recommended `.yaml` file extension (https://www.yaml.info/learn/bestpractices.html#file) ([dc3dc1a](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/dc3dc1aa798a009644f938ef41df02f370e09466))
* various changes to formatting and example rules ([b9b2366](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/b9b236645ad961cd7a8886c1697b27f3694ee047))

## 1.0.0 (2025-05-07)


### Features

* complete minimal workflow as template ([2348055](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/234805535a6353a3db59d5bba0a4b38fe8194d97))
* complete, reproducible example workflow ([1dfa7ad](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/1dfa7adb0120880ae5e85c57551d5e698a057497))
* larger update to feature fully-functional example and github actions ([93c08fc](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/93c08fc9db2f8619af7b90784db83d18ed656f25))
* major simplification of rules, replacement of others by wrappers ([3811ef7](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/3811ef796df4fe38fb7161f9a1b06fac9db86d5b))
* major simplification of template and update docs ([81ee089](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/81ee08989857366893593a333615523f05295f87))
* replaced get genome script with simple shell command ([9208995](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/9208995b78433ce3680a0b0e453ddcf5915abcef))
* update github actions workflow in linting part ([27d53ee](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/27d53eecfad935f50bc62a30248141891a4329ee))
* update github actions workflow. check formatting of yaml files using prettier ([9f5131b](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/9f5131bf0eeaf1eb7fb0937b2840f73db2a02724))
* updated all GH actions to latest versions ([4d7b3a2](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/4d7b3a2b143c304b6dcf487664c392c4a5e98f74))
* updated github actions workflow ([fd36648](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/fd3664841b830ae670549aabb214eb6004aa696d))
* updated github actions workflow ([7a3a40e](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/7a3a40e62df01b37a802a085e7210014eb3fba82))


### Bug Fixes

* 2nd attempt to fix release please wf ([f81847f](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/f81847fdfd39d99e795006da4f84701ee6ba8ddc))
* added usage docs ([776b97e](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/776b97e3d0e928d98f4c48e619090b47f702dcab))
* all-temp needs explicit input of multiqc zip dirs ([026c35a](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/026c35aebfb140746bc823ce06327e25c9a40cf1))
* change release type to 'go', fixes release please wf ([658c784](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/658c784ab5d70b117ce9dd386f5b07f8e4ff782d))
* change release type to 'go', fixes release please wf ([a81ab9d](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/a81ab9def05667e23c5e59ac881c7a57b9f1b767))
* code review issues ([97faf1a](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/97faf1ae8bde189094e6b46568f3911f01b625fd))
* dont remove temp files for test runs ([0c2c8d1](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/0c2c8d19c51648872d09a8f697826b9445bafc81))
* formatting, logging ([d6c819e](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/d6c819efcadde1ad4af342152d3aef2a982983d0))
* lint error and docs update ([cf59f11](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/cf59f11acc11c01866ad56971fd132661f4f32be))
* removed unused templates, update catalog yml ([b5c292f](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/b5c292ff4b476441d8068ca8013e3b931d30fc04))
* snakefmt error ([70d670a](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/70d670a91c79c0a9d89c59fff6add3f1036753a3))
* update release-please GH workflow ([1dad25d](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/1dad25da5de222982b0cdf35a91be6ecc5a81a42))
* update release-please GH workflow ([0ea4df2](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/0ea4df2f746e0fc760c06a3b902e2ee8bdf2ff42))
* update snakemake action ([fac8662](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/fac8662193fa501fdfc2f3bb94e7549b96dec500))
* updated schemas and params docs ([facf377](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/facf377a7cc107b3e8db0793b21027a9f3df0eeb))
* updates to enable release-please action again ([8d9552b](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/8d9552b8369ca6b115ee00777f45cf641312dde3))
* various changes to formatting and example rules ([b9b2366](https://github.com/snakemake-workflows/snakemake-workflow-template/commit/b9b236645ad961cd7a8886c1697b27f3694ee047))
