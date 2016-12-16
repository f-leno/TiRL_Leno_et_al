sh stopAll.sh

#python experiment.py -a Dummy -it 842 -et 1000 -n 3 -t 1000 -p 1 &
#python experiment.py -a SAQL -it 515 -et 750 -n 3 -t 1000 -p 1 &
#python experiment.py -a SAQL -it 837 -et 1000 -n 3 -t 1000 -p 1 &
python experiment.py -a MAQL -it 840 -et 842 -n 3 -t 1000 -p 1 &
python experiment.py -a MAQL -it 843 -et 845 -n 3 -t 1000 -p 1 &
python experiment.py -a MAQL -it 846 -et 848 -n 3 -t 1000 -p 1 &
python experiment.py -a MAQL -it 849 -et 850 -n 3 -t 1000 -p 1 &
#python experiment.py -a DQL -it 1 -et 500 -n 3 -t 1000 -p 1 &
#python experiment.py -a DQL -it 1 -et 1000 -n 3 -t 1000 -p 1 &
#python experiment.py -a DOOQ -it 994 -et 1000 -n 3 -t 1000 -p 1 &
#python experiment.py -a DOOQ -it 827 -et 850 -n 3 -t 1000 -p 1 &


