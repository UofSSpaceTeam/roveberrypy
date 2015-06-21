%% How to use:
% "PCA_terrain.png" is paint or something similar. Using a tool which draws
% pure black, draw the terrain you'd like to evaulate using pca (use the 
% pencil tool in MS Paint).
% Tips:
% - PCA is used to reduce the dimension of the problem to 1D. If you draw
% something that obviosuly cant be approximated as linear then the result
% wont be correct. 




%% -----------------------------------------------------------------------
A = imread('matlab_test.png');


A = 255 - A(:,:,1);
close all


SIZE_A = size(A);
SIZE_Y = SIZE_A(1);
SIZE_X = SIZE_A(2);

k = 1;

for i = 1 : SIZE_Y
    for j = 1 : SIZE_X
        if(A(i,j) == 255)
            y(k) = SIZE_Y - i;
            x(k) = j - 1;
            k = k + 1;
        end 
    end 
end
K = 6;


data = [x;y]';

[idx,c] = kmeans(data,K);




plot(x,y,'.',c(:,1),c(:,2),'ko')

