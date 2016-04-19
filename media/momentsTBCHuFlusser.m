%----------------------------------------------------------------
%Obtiene los momentos de Hu
%Se recibe una imagen binaria que contiene un solo objeto
function phi=momentsTBCHuFlusser(objectimage,maxorder)
[objectHeight,objectWidth]=size(objectimage);%Se obtienen caracteristicas de la imagen obtenida
%----------------------------------------------------------------
order=maxorder+1;
m=zeros(order);
mu=zeros(order);
n=zeros(order);
%----------------------------------------------------------------
%Calculo de momentos generales discretos
for h=1:objectHeight,
    for j=1:objectWidth,
        for r=1:order,
            for s=1:order,
                if objectimage(h,j)==1
                    m(r,s)=m(r,s)+(h^(r-1))*j^(s-1);       
                end
            end
        end   
    end
end
%----------------------------------------------------------------
%Calculo de centroides
if m(1,1)==0
    centroidI=0;
    centroidJ=0;
else
    centroidI=m(2,1)/m(1,1);
    centroidJ=m(1,2)/m(1,1);
end;
%----------------------------------------------------------------
%Calculo de momentos invariantes a traslaciones
for h=1:objectHeight,
    for j=1:objectWidth,
        for r=1:order,
            for s=1:order,
                if objectimage(h,j)==1
                    mu(r,s)=mu(r,s)+((h-centroidI)^(r-1))*(j-centroidJ)^(s-1);       
                end
            end
        end   
    end
end
%----------------------------------------------------------------
%Calculo de momentos invariantes a traslaciones y a escalas (etha)
for r=1:order,
    for s=1:order,
        if (r+s)>=4
            if mu(1,1)==0
                n(r,s)=0;
            else
                n(r,s)=mu(r,s)/(mu(1,1)^((r+s)/2.0));%(r+s-2)/2+1=(r+s)/2
            end;
        end
    end
end
%----------------------------------------------------------------
%Cálculo de momentos invariantes a traslaciones, rotaciones y cambios de
%escala de Hu
phi=zeros(1,8);
phi(1)=n(3,1)+n(1,3);
phi(2)=(n(3,1)-n(1,3))*(n(3,1)-n(1,3))+4*n(2,2)*n(2,2);
phi(3)=(n(4,1)-3*n(2,3))*(n(4,1)-3*n(2,3))+(3*n(3,2)-n(1,4))*(3*n(3,2)-n(1,4));
%Cálculo de momentos invariantes a traslaciones, rotaciones y cambios de
%escala de Flusser
phi(8)=n(5,1)+2*n(3,3)+n(1,5);