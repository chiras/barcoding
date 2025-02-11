awk '{ print $9 "\t" $4 "\t" $10}' all.fa.vsearch-viri.out | sed "s/[a-zA-Z0-9_,;:=-]*s://"  > all.fa.vsearch-viri.out.fm
awk '{ print $9 "\t" $4 "\t" $10}' all.fa.vsearch-sebas.out  | sed "s/[a-zA-Z0-9_,;:=-]*s://" > all.fa.vsearch-sebas.out.fm
cut -f 1,4 all.fa.vsearch-sintax.out >  all.fa.vsearch-sintax.out.fm
awk '{ print $1 "\t" $2 "\t" $4/$3 "\t" $5}' all.fa.blast-viri.out | sed "s/[a-zA-Z0-9_,;:=-]*s://"  > all.fa.blast-viri.out.fm
awk '{ print $1 "\t" $2 "\t" $4/$3 "\t" $5}' all.fa.blast-sebas.out | sed "s/[a-zA-Z0-9_,;:=-]*s://"  >  all.fa.blast-sebas.out.fm
awk '{ print $1 "\t" $2 "\t" $4/$3 "\t" $5 $6}' all.fa.blast-remote.out | sed "s/[a-zA-Z0-9_,;:=-]*s://"  >  all.fa.blast-remote.out.fm