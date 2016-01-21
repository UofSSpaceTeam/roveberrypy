close all
load('../scratch/output.csv');
x = output(:,1);
y = output(:,2);

%PLOT ON AXES
plot(x,y);
title('Rover Drive Path');
xlabel('Relative Position, [m]')
ylabel('Relative Position, [m]')
axis equal
grid on