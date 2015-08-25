using System;
using System.Windows;
using System.Windows.Controls;
using System.Collections.Generic;
using System.Diagnostics;
using System.Threading;
using System.Windows.Media;

using StateElement = System.Collections.Generic.KeyValuePair<string, dynamic>;
using StateDict = System.Collections.Generic.Dictionary<string, dynamic>;

namespace usstgui
{
    public partial class EditorWindow : Window
    {

        public EditorWindow()
        {
            InitializeComponent();
        }

		private void readValue(object sender, RoutedEventArgs e)
		{
			string key = keyBox.Text;
			dynamic value = SharedState.get(keyBox.Text);
			if(value == null)
			{
				readButton.Background = new SolidColorBrush(Colors.Coral);
				return;
			}
			readButton.Background = new SolidColorBrush(Colors.LightGreen);
			valueBox.Text = getValueString(value);
			
			Type t = getValueType(value);
			if(t == null)
			{
				stringButton.IsChecked = false;
			}

			if(t.Equals(typeof(String)))
				stringButton.IsChecked = true;
			else if(t.Equals(typeof(Int64)))
				integerButton.IsChecked = true;
			else if(t.Equals(typeof(Double)))
				floatButton.IsChecked = true;
			else if(t.Equals(typeof(Boolean)))
				booleanButton.IsChecked = true;
		}

		private Type getValueType(dynamic value)
		{
			try
			{
				return value.GetType();
			}
			catch
			{
				return null;
			}
		}

		private string getValueString(dynamic value)
		{
			try
			{
				if(value == null)
					return "null";
				else
					return value.ToString();
			}
			catch
			{
				return "ERROR";
			}
		}

		private void writeValue(object sender, RoutedEventArgs e)
		{
			string strVal = valueBox.Text;
			dynamic value = null;
			if((bool)stringButton.IsChecked)
				value = strVal;
			try
			{
				if((bool)integerButton.IsChecked)
					value = Int64.Parse(strVal);
				else if((bool)floatButton.IsChecked)
					value = Double.Parse(strVal);
				else if((bool)booleanButton.IsChecked)
					value = Boolean.Parse(strVal);
				SharedState.set(keyBox.Text, value);
				writeButton.Background = new SolidColorBrush(Colors.LightGreen);
			}
			catch
			{
				writeButton.Background = new SolidColorBrush(Colors.Coral);
			}
		}
	}
}
