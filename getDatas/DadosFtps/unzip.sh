 #!/bin/bash  
for z in *.ex_; do 
    unzip "$z";
    mv "$(unzip -Z1 $z)" "${z%%.*}.txt";
    mv "${z%%.*}.txt" "extraidos" ;
done

	