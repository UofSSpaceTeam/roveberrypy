#ifndef ARM2016_INVKIN
#define ARM2016_INVKIN


void CalculatePositions(double r, double z) {
    double L1 = 352.12;
    double L2 = 569;
    double L1_p2 = L1*L1;
    double L1_p3 = L1*L1*L1;
    double L1_p4 = L1*L1*L1*L1;
    double L2_p2 = L2*L2;
    double L2_p3 = L2*L2*L2;
    double phi1 = acos((L1_p3 * z + L1 * z * (-L2_p2+r_p2+z_p2)+(r_p2+z_p2) *
    sqrt(-((L1_p2 * r_p2 * (L1_p4+(-L2_p2+r_p2+z_p2)*(-L2_p2+r_p2+z_p2)-2 * L1_p2 *
    (L2_p2+r_p2+z_p2)))/((r_p2+z_p2)*(r_p2+z_p2)))))/(2 * L1_p2 * (r_p2+z_p2)));
    double phi2 = acos(-1*((L1_p3 * z-L1 * z * (L2_p2+r_p2+z_p2)+(r_p2+z_p2) *
    sqrt(-1*((L1_p2 * r_p2 * (L1_p4+(-L2_p2+r_p2+z_p2)*(-L2_p2+r_p2+z_p2)-2 * L1_p2 *
    (L2_p2+r_p2+z_p2)))/((r_p2+z_p2)*(r_p2+z_p2)))))/(2 * L1 * L2 * (r_p2+z_p2))));


    double x0 = 127.44;
    double H = 347.9;
    double phi_c = 1.1383;
    double S = 170;
    double pos1 = x0*x0 + H*H - 2*x0*H*cos(PI/2+phi1-phi_c);
    double pos2 = L1_p2 + S*S - 2*L1*S*cos(phi1 + PI - phi2);

    g_destination[3] = pos1;
    g_destination[4] = pos2;
}


#endif
