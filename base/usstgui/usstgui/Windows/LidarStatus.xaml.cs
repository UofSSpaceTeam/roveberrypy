using System;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Shapes;

namespace usstgui
{
    public partial class LidarStatus : Window
    {
        const int PANEL_SIZE = 500;
        double m_outer_radius; // m
        enum ZOOM{IN, OUT };
        const int PTS_PER_ROT = 100;
        int m_positionIndex;
        
        class lidarDataPoint
        {
            public lidarDataPoint(double dist, double ang)
            {
                distance = dist;
                angle = ang;
            }
            public void setDistance(double dist)
            {
                distance = dist;
            }
            public void setAngle(double ang)
            {
                angle = ang;
            }
            public double distance;
            public double angle;
        };
        
        lidarDataPoint[] m_data = new lidarDataPoint[PTS_PER_ROT];

        public Ellipse LidarPoint(double radius, double theta)
        {
            const int PT_RADIUS = 4;
            Ellipse ptObj = new Ellipse();
            ptObj.Width = 2*PT_RADIUS;
            ptObj.Height = 2*PT_RADIUS;
            radius = getMetersToDigi(radius);
            double x = PANEL_SIZE / 2 + (int)(radius * Math.Sin(theta) + 0.5) - PT_RADIUS;
            double y = PANEL_SIZE / 2 - (int)( radius * Math.Cos(theta) + 0.5 ) - PT_RADIUS;
            ptObj.Margin = new Thickness(x, y, 0.0, 0.0);
            SolidColorBrush fillBrush = new SolidColorBrush();
            fillBrush.Color = Color.FromArgb(255,255,0,0);
            ptObj.Fill = fillBrush;
            if (radius > 250)
            {
                ptObj.Visibility = Visibility.Hidden;
            }
            return ptObj;
        }
        private void setZoom(ZOOM direction)
        {
            if(m_outer_radius > 3 || direction == ZOOM.OUT) {
                if(m_outer_radius == 5 && direction == ZOOM.IN) {
                    m_outer_radius = 3;
                } else if(m_outer_radius == 50 && direction == ZOOM.OUT) {
                    // DO NOTHING
                } else if(direction == ZOOM.IN) {
                    m_outer_radius -= 5;
                } else if(m_outer_radius == 3 && direction == ZOOM.OUT) {
                    m_outer_radius = 5;
                } else {
                    m_outer_radius += 5;
                }

                Label1.Text = m_outer_radius.ToString() + "m";
                Label2.Text = (m_outer_radius*0.8).ToString() + "m";
                Label3.Text = (m_outer_radius*0.6).ToString() + "m";
                Label4.Text = (m_outer_radius*0.4).ToString() + "m";
                Label5.Text = (m_outer_radius*0.2).ToString() + "m";

            } else {

            }
        }
        private double getMetersToDigi(double m){
            double val =  m * (PANEL_SIZE / 2 / m_outer_radius);
            return val;
        }

        public LidarStatus()
        {
            InitializeComponent();

            m_outer_radius = 5;
            setZoom(ZOOM.OUT);
            inializeLidarArray();
            updateDrawing();
            m_positionIndex = 0;

            for(int idx = 0; idx < 4; idx++)
            {
                pushLidarReading(2*idx, 0.866);
            }
            
            

        }
        public void inializeLidarArray()
        {
            for (int idx = 0; idx < PTS_PER_ROT; idx++)
            {
                m_data[idx] = new lidarDataPoint(10, 0);
            }
        }

        public void pushLidarReading(double distance, double position)
        {
            m_data[m_positionIndex].distance = distance;
            m_data[m_positionIndex].angle = position;
            m_positionIndex = (m_positionIndex + 1) % PTS_PER_ROT;
            updateDrawing();
        }

        public void updateDrawing()
        {
            drawSpace.Children.Clear();
            for(int idx = 0; idx < PTS_PER_ROT; idx++)
            {
                drawSpace.Children.Add(LidarPoint(m_data[idx].distance, m_data[idx].angle));
            }
        }
        private void btn_ZIN_Click(object sender, RoutedEventArgs e)
        {
            setZoom(ZOOM.IN);
            updateDrawing();
        }

        private void btn_ZOUT_Click(object sender, RoutedEventArgs e)
        {
            setZoom(ZOOM.OUT);
            updateDrawing();
        }
    }
}
