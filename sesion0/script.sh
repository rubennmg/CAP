#!/bin/bash
host=`hostname`
hora=`date`
FICHERO=/scratch/$LOGNAME_$RANDOM
echo "Fichero: $FICHERO" > $FICHERO
echo "Usuario logname: $LOGNAME" >> $FICHERO
echo "Home: $HOME" >> $FICHERO
echo "Hora ejecución: $hora" >> $FICHERO
echo "Nodo de cálculo: $host" >> $FICHERO
echo "HOLA" >> $FICHERO
sleep 20
echo "ADIOS" >> $FICHERO
mv $FICHERO $HOME