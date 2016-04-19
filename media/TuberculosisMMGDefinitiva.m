% Registered by Guillermo Forero Manuel Vargas and Gabriel Cristobal
% Program for image analysis tuberculosis. This program gets
% Descriptors of objects used to train the system and
% Stored in the file.
% Is assumed that each image contains only a bacillus learning.
% July 21, 2004, used for IEEE article.
% This program is the definitive version MMG. It is based on the use of
% The Hu1 to hu3, Hu11 for eccentricity and classification and filtering area for descriptors
function TuberculosisMMGDefinitiva(namafile)
close all;
clc;
%MURE%
%[fileName,pathname]=uigetfile('*.bmp','Pick the samples bmp-files', 'MultiSelect', 'on');%Abre ventana de dialogo
currentFolder = pwd;
pathname = strcat(currentFolder, '\929_Positive_binarized_edited\*.bmp');
d = dir(pathname);
fileName = {d.name}';
pathname = strcat(currentFolder, '\929_Positive_binarized_edited\');
%currentFolder = pwd;
%pathname = strcat(currentFolder, '\929_Positive_binarized_edited\');
if isequal(fileName,0)|isequal(pathname,0)
    disp('User pressed cancel')
    return;
else
    %----------------------------------------------------------------
    %Se crea titulos de descriptores
    descriptorsname={'Excentricidad' 'Compacidad' 'Phi1' 'Phi2' 'Phi3' 'Phi4' 'Phi5' 'Phi6' 'Phi7' 'Phi8'};
    %----------------------------------------------------------------
    %Se obtienen los descriptores de todos los objetos de entrenamiento
    objectsnumber=max(size(fileName));%Total de objetos de entrenamiento
    objects=zeros(objectsnumber,10);%Objects contiene el total de objetos usados en el entrenamiento
    for k=1:objectsnumber,%Para el total de archivos ..
        %disp(['User selected ',fullfile(pathname,fileName{k})])
        image=imread(fullfile(pathname,fileName{k}));
        objects(k,:)=tuberculosetraining(image);
    end;
    %----------------------------------------------------------------
    %Se reduce el numero de descriptores.
    objects=objects(:,[3:5 10]);
    %----------------------------------------------------------------
    %Se obtienen los centroides de las clases usando el k-means.
    classesnumber=4;
    descriptorsnumber=size(objects,2);
    %----------------------------------------------------------------
    %Aplicacion de los modelos gaussianos mixtos para la construccion de
    %las funciones de densidad de probabilidad de la clase bacilos.
    mix=gmm(descriptorsnumber,classesnumber,'full');
    options=foptions;
    mix=gmminitmod(mix,objects,options);%Inicializacion del gmm con centroides obtenidos de k-means.
    options(1)=1;% Prints out error values.
    options(5)=1;%A covariance matrix is reset to its original value when any of its singular values are too small
    options(14)=300;% Max. number of iterations.
    mix=gmmem(mix,objects,options);
    m=mix.centres
    c=mix.covars;
    %----------------------------------------------------------------
    %Se abren imagenes a analizar
    %MURE
    currentFolder = pwd;
    pathname = strcat(currentFolder, '\target\');
    d = dir(pathname);
    %fileName = {d(~cellfun(@isempty,regexpi({d.name},'.*(bmp|jpg)'))).name};
    fileName = {namafile};
    pathname = strcat(currentFolder, '\target\');
    %[fileName,pathname]=uigetfile('*.bmp;*.tif','Pick one or more bmp or tiff files', 'MultiSelect', 'on');%Abre ventana de dialogo
    if isequal(fileName,0)|isequal(pathname,0)
        disp('User pressed cancel')
    return;
    else
        %----------------------------------------------------------------
        %Calculo de matriz de covarianza y su inversa para uso en la
        %distancia de Mahalanobis
        for class=1:classesnumber%calculo matrices de covarianza inversas
            covarianza(:,:)=double(c(:,:,class));%Tecnica GMM
            cinv(class,:,:)=inv(covarianza);
            threshold(class)=-4.6182-.5*log(det(covarianza(:,:)))+log(mix.priors(class));%0.1
%           threshold(class)=-5.5352-.5*log(det(covarianza(:,:)))+log(mix.priors(class));%0.05
%            threshold(class)=-8.37482-.5*log(det(covarianza(:,:)))+log(mix.priors(class));%0.005
%            threshold(class)=-12.8724-.5*log(det(covarianza(:,:)))+log(mix.priors(class));%0.0001
%0.001:20.5150,0.0005:22.1053,0.0001:25.7448        
        end;    
        threshold
        %----------------------------------------------------------------
        for k=1:max(size(fileName)),%Para el total de archivos ..
            disp(['User selected ',fullfile(pathname,fileName{k})])
            image=imread(fullfile(pathname,fileName{k}));
            bacilos=0;
            examen=0;%Examen negativo
            %----------------------------------------------------------------
            candidates=tuberculoseclassification(image);%Obtiene los objetos candidates a ser clasificados como bacilos o no
            %----------------------------------------------------------------
            %Se mira si hay objetos en la imagen
            candidatesnumber=size(candidates,1);
            if candidatesnumber~=1|candidates(1,2)~=0%Si hay objetos continua
            %----------------------------------------------------------------
            %Si hay objetos, se reduce el numero de descriptores.
%            candidatos=candidates(:,[3:5 10 2]);
            candidatos=candidates(:,[3:5 10]);
            %----------------------------------------------------------------
            %Clasificacion Mahalanobis
            for candidate=1:candidatesnumber
                for class=1:classesnumber
                    a(:,:)=cinv(class,:,:);
                    distance(1,class)=[(candidatos(candidate,:)-m(class,:))*a*(candidatos(candidate,:)-m(class,:))'];
            end;
            %----------------------------------------------------------------
            [mindistance,pos]=min(distance);%Se determina la distancia minima entre el objeto y una clase
            %----------------------------------------------------------------
            if mindistance<threshold(pos)%Si la distancia es menor al umbral el objeto es asignado a una clase.
                bacilos=bacilos+1;
            end;
        end;
            bacilos
            if bacilos
                examen=1;%positivo
            end;
        %examen
        end;%if candidatesnumber~=1|candidates(1,2)~=0
        %----------------------------------------------------------------
        

        %MURE
        %disp(strcat('mama', num2str(bacilos)));
        currentFolderWrite = pwd;
        pathnameWrite = strcat(currentFolderWrite, '\result\');
        sourceFile = strcat(pathname, fileName{k});
        destFile = strcat(pathnameWrite, strcat(strcat(num2str(bacilos), '_'), fileName{k}));
        copyfile(sourceFile, destFile);

        delete(sourceFile);
        
        disp(sourceFile);
        disp(destFile);
        
        exit;
        end;%for
    %----------------------------------------------------------------
    end
end

%----------------------------------------------------------------
function objects=tuberculoseclassification(image)
%----------------------------------------------------------------
%Habilitar la segmentacion de la imagen y el cerrado cuando la imagen entrante es rgb y no binaria
%greyimage=rgb2gray(image);%Obtiene imagen canal Y.
greenimage=image(:,:,2);%Obtiene imagen canal verde
greyimage=greenimage;
umbralBackground=double(mean(mean(greenimage)));%Obtiene color promedio de la imagen verde
maxUmbral=double(max(max(greenimage)));%Obtiene color maximo de la imagen verde
%imshow(greyimage);
%pause;
%----------------------------------------------------------------
%Aplicacion de filtro de derivacion de Deriche
%smoothimage=derichelowpass(greyimage,1);
%gradientimage=derichemagnitudegradient(greyimage,1);
%[gradientimage,gradX,gradY]=derichegradient(greyimage,1);
%imshow(gradientimage);
%pause;
%----------------------------------------------------------------
[edgeimage,thresh]=edge(greyimage,'canny',0.5);
%imshow(edgeimage);
%pause;
%----------------------------------------------------------------
%Cerrado de la imagen
se=strel('square',3);%'disk',2);
closeimage=imclose(edgeimage,se);
%imshow(closeimage);
%pause;
%extrema=extremalocal(gradX,gradY);
%----------------------------------------------------------------
%Se rellenan las zonas cerradas
fillimage=imfill(closeimage,'holes');
%imshow(fillimage);
%pause;
%----------------------------------------------------------------
%Se eliminan los pixeles aislados y lineas que puedan quedar
openimage=imopen(fillimage,se);
%imshow(openimage);
%pause;
%----------------------------------------------------------------
%Crea imagen etiquetada
labelimage=bwlabel(openimage,8);
%----------------------------------------------------------------
%Obtiene el numero de regiones conectadas en la imagen
labelNumber=max(max(labelimage));
%----------------------------------------------------------------
%Eliminacion de objetos en la imagen cuyo color no sea de bacilo
stats=regionprops(labelimage,'PixelList');%Se obtiene las listas de pixeles de cada region
idx=0;
a=1;
umbralBackground=3*(maxUmbral-umbralBackground)/5+umbralBackground;
for label=1:labelNumber
    pixels=stats(label).PixelList;%se obtienen coordenadas del pixel en la lista
    for i=1:size(pixels,1)
        if image(pixels(i,2),pixels(i,1),2)>umbralBackground&(image(pixels(i,2),pixels(i,1),2)>image(pixels(i,2),pixels(i,1),1))
            idx(a)=label;
            a=a+1;
            break;
        end;
    end;
end;
if a==1%Si no hay objetos en la imagen..
    disp('No hay objetos en la imagen');
    objects=zeros(1,10);%Se crea un falso objeto, cuyos descriptores son cero
    %y hace el objeto eliminable por compacidad
    return;
end;
shapesimage=ismember(labelimage,idx);
%imshow(shapesimage);
%pause;
%----------------------------------------------------------------
%Crea imagen etiquetada de los objetos
labelimage=bwlabel(shapesimage,8);
%----------------------------------------------------------------
%Se aplica un filtro sobre los objetos a estudiar de acuerdo a su area y
%excentricidad.
%Obtiene regiones con area mayor a 42 puntos y menor a 208, y excentricidad
%mayor a 0.8741.
stats=regionprops(labelimage,'Area','Eccentricity');
idx=find([stats.Area]>=43&[stats.Area]<=207&[stats.Eccentricity]>0.8924);
shapesimage=ismember(labelimage,idx);
%----------------------------------------------------------------
%Crea nueva imagen etiquetada de los contornos restantes
labelimage=bwlabel(shapesimage,8);
%Obtiene el numero de regiones conectadas en la imagen
labelNumber=max(max(labelimage));
objects=zeros(labelNumber,10);%Se crean los objetos
if labelNumber==0%Si no hay objetos en la imagen..    
    disp('No hay objetos de tamaño adecuado en la imagen');
    objects=zeros(1,10);%Se crea un falso objeto, cuyos descriptores son cero
    %y hace el objeto eliminable por compacidad
    return;
end;
%----------------------------------------------------------------
%Obtiene descriptores de objetos de interes
%RGB = label2rgb(labelimage,@jet,'k');
%imshow(RGB,'notruesize')
stats=regionprops(labelimage,'Eccentricity','Image');
%----------------------------------------------------------------
for label=1:labelNumber,
    %----------------------------------------------------------------
    %Se cargan los descriptores obtenidos
    objects(label,1)=stats(label).Eccentricity;
    %----------------------------------------------------------------
    %Se obtiene imagen del objeto obtenido
    objectimage=stats(label).Image;%Se obtiene imagen de objeto
    %imshow(objectimage);
    %pause;%Se verifica que la imagen desplegada corresponda al objeto de interes
    %----------------------------------------------------------------
    %Obtiene los momentos de Hu
    objects(label,3:10)=momentsTBCHuFlusser(objectimage,4);
    objects(label,2)=1;%No hace el objeto eliminable por compacidad
end