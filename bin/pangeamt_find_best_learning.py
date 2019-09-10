from pangeamt_toolkit import Pangeanmt

#TODO intervals de prova

for i in intervals:
    config = gen_config() #TODO will have to overwrite the config file
    p = Pangeanmt(dir) #TODO
    for seg in file: #TODO
        outfile.write(p.translate(seg))

    #TODO train the model with all the segments
    #TODO translate again all the segments
    #TODO Calculate BLEU
