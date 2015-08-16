using System;
using System.Windows;
using System.Windows.Controls;
using System.Collections.Generic;
using System.Diagnostics;
using System.Threading;

using StateElement = System.Collections.Generic.KeyValuePair<string, dynamic>;
using StateDict = System.Collections.Generic.Dictionary<string, dynamic>;

namespace usstgui
{
    public partial class DataWindow : Window
    {
		struct watchedItem
		{
			public Label keyLabel;
			public Label valueLabel;
			public Button remover;
		}

		List<watchedItem> itemList = new List<watchedItem>();

        public DataWindow()
        {
            InitializeComponent();
			new Thread(new ThreadStart(valueUpdater)).Start();
        }

		private void addItem(object sender, RoutedEventArgs e)
		{
			watchedItem item = new watchedItem();
			item.keyLabel = new Label();
			item.keyLabel.Content = inputBox.Text;
			item.valueLabel = new Label();
			item.remover = new Button();
			item.remover.Width = 28;
			item.remover.Height = 28;
			item.remover.Content = "X";
			item.remover.Click += removeItem;
			windowGrid.Children.Add(item.keyLabel);
			Grid.SetColumn(item.keyLabel, 0);
			windowGrid.Children.Add(item.valueLabel);
			Grid.SetColumn(item.valueLabel, 1);
			windowGrid.Children.Add(item.remover);
			Grid.SetColumn(item.remover, 2);
			itemList.Add(item);
			redraw();
		}

		private void editItem(object sender, RoutedEventArgs e)
		{
			new EditorWindow().Show();
		}

		public void removeItem(object sender, RoutedEventArgs e)
		{
			foreach(watchedItem item in itemList)
			{
				if(sender.Equals(item.remover))
				{
					itemList.Remove(item);
					windowGrid.Children.Remove(item.keyLabel);
					windowGrid.Children.Remove(item.valueLabel);
					windowGrid.Children.Remove(item.remover);
					redraw();
					return;
				}
			}
		}

		private void redraw()
		{
			while(windowGrid.RowDefinitions.Count > 2)
			{
				windowGrid.RowDefinitions.RemoveAt(windowGrid.RowDefinitions.Count - 1);
			}

			while(windowGrid.RowDefinitions.Count < itemList.Count + 2)
			{
				RowDefinition newRow = new System.Windows.Controls.RowDefinition();
				newRow.Height = new GridLength(28);
				windowGrid.RowDefinitions.Add(newRow);
			}

			int row = 2;
			foreach(watchedItem item in itemList)
			{

				item.valueLabel.Content = getValueString((string)item.keyLabel.Content);
				Grid.SetRow(item.keyLabel, row);
				Grid.SetRow(item.valueLabel, row);
				Grid.SetRow(item.remover, row);
				row++;
			}
		}

		private void valueUpdater()
		{
			while(true)
			{
				foreach(watchedItem item in itemList)
				{
					this.Dispatcher.Invoke((Action)(() => { item.valueLabel.Content = getValueString((string)item.keyLabel.Content); }));
				}
				Thread.Sleep(250);
			}
		}

		private string getValueString(string key)
		{
			try
			{
				dynamic value = SharedState.get(key);
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
	}
}
