%% How to use:
% Create a png file named "PCA_terrain.png" in MS Paint or something 
% similar. The image should be something like 100x50. Using the pencil
% tool, draw the terrain you want to find the best straight line through.

% Tips:
% - run first section of the code to see the PCA decomp
% - run the second section of the code to see the best guess at where to
% pass through a gap.
% - PCA is used to reduce the dimension of the problem to 1D. If you draw
% something that obviosuly cant be approximated as linear then the result
% wont be correct. 
% - later on if we decided to look at using PCA this could be handled by
% looking at clusters in teh pc2 axis and the evaulatign the pca somewhat
% recurivley to break a purely 2D problem into a path of 1D problems.


%%
clear all
A = imread('PCA_terrain.png');
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

[c,s] = pca([x;y]');

len = sqrt((x(end)-x(1))^2 + (y(end)-y(1))^2);

% center
x0 = (x(end) + x(1))/2;
y0 = (y(end) + y(1))/2;

pca_line = c*[-len/2, len/2; 0, 0];

xx = pca_line(1,:) + x0;
yy = pca_line(2,:) + y0;

perp = [0,-1;1,0]*c*[-len/3, len/3; 0, 0];

xx_p = perp(1,:) + x0;
yy_p = perp(2,:) + y0;


subplot(3,1,1)
p1 = plot(x,y,'.',xx,yy,'g-',xx_p,yy_p,'r-');
axis equal


subplot(3,1,2)
p2 = plot(s(:,1),0,'.');


subplot(3,1,3)
p2 = plot(s(:,2),0,'.');

set(p1,'Markersize',15);
set(p2,'Markersize',15);

%%

sorted_x = sort(s(:,1));

diff = sorted_x(2:length(x),1) - sorted_x(1:length(x)-1,1);

diff_max = find(diff == max(diff));

x1 = find(s(:,1) == sorted_x(diff_max));
x2 = find(s(:,1) == sorted_x(diff_max+1));

subplot(3,1,1)

best = [(x(x2) + x(x1))/2,(y(x2) + y(x1))/2 ];

p1 = plot(x,y,'.')
hold all
p2 = plot(best(1),best(2),'mx','Markersize',25);
axis equal




