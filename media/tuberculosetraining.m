%Desarrollado por Manuel Guillermo Forero Vargas
function objects=tuberculosetraining(image)
%----------------------------------------------------------------
%Obtiene contorno de los objetos en la imagen
%imshow(image);
%pause;
%perimeterimage=bwperim(image);
negativeimage=imcomplement(image);
%Crea imagen etiquetada de los contornos
labelimage=bwlabel(negativeimage,8);
%RGB = label2rgb(labelimage,@jet,'k');
%imshow(RGB,'notruesize')
%pause;
%----------------------------------------------------------------
%Obtiene el numero de regiones conectadas en la imagen
labelNumber=max(max(labelimage));
%----------------------------------------------------------------
%Obtiene regiones con contorno mayor a 50 puntos
stats=regionprops(labelimage,'Area');
idx=find([stats.Area]>10&[stats.Area]<200);
shapesimage=ismember(labelimage,idx);
%----------------------------------------------------------------
%Crea nueva imagen etiquetada de los contornos restantes
labelimage=bwlabel(shapesimage,8);
%Obtiene el numero de regiones conectadas en la imagen
labelNumber=max(max(labelimage));
if labelNumber>1
    disp('Advertencia: Mas de un objeto en la imagen');
elseif labelNumber==0
    disp('Grave: No hay objetos en la imagen');
end
%----------------------------------------------------------------
%Se cargan los descriptores obtenidos
objects=zeros(1,10);
%----------------------------------------------------------------
%Se obtiene la imagen rellena del objeto
%RGB = label2rgb(labelimage,@jet,'k');
%imshow(RGB,'notruesize')
stats=regionprops(labelimage,'FilledImage');
objectimage=stats(1).FilledImage;
%----------------------------------------------------------------
%Obtiene descriptores de objetos de interes.
%Se calcula la excentricidad sobre el objeto relleno y no solo sobre su
%contorno, pues los resultados son diferentes y en la clasificacion se
%calcula la excentricidad sobre el objeto relleno.
labelimage=bwlabel(objectimage,8);%Crea imagen etiquetada del objeto relleno.
%imshow(objectimage);
%pause;%Se verifica que la imagen desplegada corresponda al objeto de interes
%----------------------------------------------------------------
%Obtiene los momentos de Hu
objects(3:10)=momentsTBCHuFlusser(objectimage,4);%pho=humoments(objectimage);