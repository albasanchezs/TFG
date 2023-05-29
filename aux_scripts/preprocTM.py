"""
Carries out specific preprocessing for TM.
"""

import argparse
import datetime as DT
import json
import logging
import multiprocessing as mp
import sys
import time
import warnings
from pathlib import Path
from subprocess import check_output

sys.path.append('../')
warnings.filterwarnings(action="ignore")

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
logger.addHandler(handler)


def main(nw=0, iter_=0, spark=True):

    # Create folder structure
    # Path("/export/usuarios_ml4ds/lbartolome/Datasets/S2CS/models_preproc_ctm")#
    #"/export/usuarios_ml4ds/lbartolome/Datasets/S2CS/models_preproc_mallet"#
    models = Path(
        "C:\Datasets\models_preproc_mallet")
    models.mkdir(parents=True, exist_ok=True)

    #en stw luego incluir una mia propia para editarla con lo que me salga. keep_n creo que es numero it.
    Preproc = {
        "min_lemas": 15,
        "no_below": 15,
        "no_above": 0.4,
        "keep_n": 100000,
        "stopwords": [
            "D:\\Alba Sánchez\\Documents\\GitHub\\TFG\\topicmodeler\\wordlists\\english_generic.json",
            "D:\\Alba Sánchez\\Documents\\GitHub\\TFG\\topicmodeler\\wordlists\\S2_stopwords.json",
            "D:\\Alba Sánchez\\Documents\\GitHub\\TFG\\topicmodeler\\wordlists\\S2CS_stopwords.json",
            "D:\\Alba Sánchez\\Documents\\GitHub\\TFG\\topicmodeler\\wordlists\\wiki_categories.json",
        ],
        "equivalences": [
            "D:\\Alba Sánchez\\Documents\\GitHub\\TFG\\topicmodeler\\wordlists\\S2_equivalences.json",
            "D:\\Alba Sánchez\\Documents\\GitHub\TFG\\topicmodeler\\wordlists\\S2CS_equivalences.json",
        ]
    }


    # Create model folder
    model_path = models.joinpath("iter_" + str(iter_))
    model_path.mkdir(parents=True, exist_ok=True)
    model_stats = model_path.joinpath("stats")
    model_stats.mkdir(parents=True, exist_ok=True)

    #la ruta a mi parquet
    #"/export/usuarios_ml4ds/lbartolome/Datasets/S2CS/preproc_scholar_embeddings.parquet"
    # Save dataset json file
    Dtset = "S2CS"
    DtsetConfig = model_path.joinpath(Dtset+'.json')
    parquetFile = Path(
        "C:\\textpreproc\dataout\\part.0.parquet")
    TrDtset = {
        "name": "unis",
        "Dtsets": [
            {
                "parquet": parquetFile,
                "source": "S2CS",
                "idfld": "iden",
                "lemmasfld": [
                    "lemmas"
                ],
                "filter": ""
            }
        ]
    }
    with DtsetConfig.open('w', encoding='utf-8') as outfile:
        json.dump(TrDtset, outfile,
                  ensure_ascii=False, indent=2, default=str)

    # Save configuration file
    configFile = model_path.joinpath("trainconfig.json")
    train_config = {
        "name": Dtset,
        "description": "",
        "visibility": "Public",
        "trainer": "mallet",
        "TrDtSet": DtsetConfig.resolve().as_posix(),
        "Preproc": Preproc,
        "TMparam": {},
        "creation_date": DT.datetime.now(),
        "hierarchy-level": 0,
        "htm-version": None,
    }
    with configFile.open('w', encoding='utf-8') as outfile:
        json.dump(train_config, outfile,
                  ensure_ascii=False, indent=2, default=str)
    #no tengo spark
    # Execute command
    """
    if spark:
        script_spark = "/export/usuarios_ml4ds/lbartolome/spark/script-spark"
        token_spark = "/export/usuarios_ml4ds/lbartolome/spark/tokencluster.json"
        script_path = './src/topicmodeling/topicmodeling.py'
        machines = 10
        cores = 5
        options = '"--spark --preproc --config ' + configFile.resolve().as_posix() + '"'
        cmd = script_spark + ' -C ' + token_spark + \
            ' -c ' + str(cores) + ' -N ' + str(machines) + \
            ' -S ' + script_path + ' -P ' + options
        print(cmd)
        try:
            logger.info(f'-- -- Running command {cmd}')
            output = check_output(args=cmd, shell=True)
        except:
            logger.error('-- -- Execution of script failed')
    else:
    """
    # Run command for corpus preprocessing using gensim
    # Preprocessing will be accelerated with Dask using the number of
    # workers indicated in the configuration file for the project
    #cmd = f'python src/topicmodeling/topicmodeling.py --preproc --config {configFile.resolve().as_posix()} --nw {str(nw)}'
    cmd = f'py topicmodeler/src/topicmodeling/topicmodeling.py --preproc --config {configFile.resolve().as_posix()} --nw {str(nw)}'
    print(cmd)

    try:
        logger.info(f'-- -- Running command {cmd}')
        output = check_output(args=cmd, shell=True)
    except:
        logger.error('-- -- Command execution failed')

    # cmd = f"python src/topicmodeling/topicmodeling.py --preproc --config #{configFile.resolve().as_posix()} --nw {str(nw)}"
    # logger.info(f"Running command '{cmd}'")

    t_start = time.perf_counter()
    check_output(args=cmd, shell=True)
    t_end = time.perf_counter()
    t_total = t_end - t_start

    logger.info(f"Total time --> {t_total}")
    print("\n")
    print("-" * 100)
    print("\n")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Preprocessing for TM')
    parser.add_argument('--nw', type=int, required=False, default=0,
                        help="Number of workers when preprocessing data with Dask. Use 0 to use Dask default")
    parser.add_argument('--iter_', type=int, required=False, default=0,
                        help="Preprocessing number of this file.")
    parser.add_argument('--spark', type=int, required=False, default=True,
                        help="Whether to use spark or Dash.")
    args = parser.parse_args()
    main(args.nw, args.iter_, args.spark)