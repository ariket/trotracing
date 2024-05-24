using System.Windows;
using System.IO;
using System.Runtime.CompilerServices;
using System.Windows.Controls;
using static System.Net.Mime.MediaTypeNames;
using System.Reflection.Metadata;


namespace trotracing
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    /// 

    public partial class MainWindow : Window
    {
        public bool DataFromATG = false;
      
        public MainWindow()
        {
            InitializeComponent();
            
            SetConsoleSettings(); //If you want to use the app without CMD remove this line and Right click
                                  //on trotracing in Solution Explorer and click on Properties and finally
        }                         //change Output type to "Windows Application" 

        private void SetConsoleSettings()
        {
            Console.SetWindowSize(130, 30);
            Console.BackgroundColor = ConsoleColor.Black;
            Console.ForegroundColor = ConsoleColor.DarkRed;
            Console.Title = "Travtipset logger (stäng ej ner denna kommandotolk under körning)";
        }

        private void About_Click(object sender, RoutedEventArgs e)
        {
            About.Visibility = Visibility.Visible;
            ComboBoxMeny.IsEnabled = false;
        }

        private void Settings_Click(object sender, RoutedEventArgs e)
        {
            NotYetImplemnted.Visibility = Visibility.Visible;
            ComboBoxMeny.IsEnabled = false;    
        }

        private void Results_Click(object sender, RoutedEventArgs e)
        {
            NotYetImplemnted.Visibility = Visibility.Visible;
            ComboBoxMeny.IsEnabled = false;
        }

        private void RaceType_Click(object sender, RoutedEventArgs e)
        {
            SelectRaceType.Visibility = Visibility.Visible;
            ComboBoxMeny.IsEnabled = false;
        }

        private void Quit_Click(object sender, RoutedEventArgs e)
        {
            Console.WriteLine("/nAppen avslutas...");
            System.Windows.Application.Current.Shutdown();
        }

        private async void RadioButton_Click(object sender, RoutedEventArgs e)
        {
            string RaceType = "V75";
            if (RadioV64.IsChecked == true)
                RaceType = "V64";
            else if (RadioV86.IsChecked == true)
                RaceType = "V86";
            
            if(await Program.GetDataFromATG(RaceType))
                DataFromATG = true;
            SelectRaceType.Visibility = Visibility.Collapsed;
            ComboBoxMeny.IsEnabled = true;
        }

        public void WriteResultATG()
        {
            stackPanel.Visibility = Visibility.Visible;
            string path = "..\\..\\..\\ATG\\data\\resultData.txt";
            string[] lines = File.ReadAllLines(path);
            for (int i = 0; i < lines.Length; i++)
            {
                textBlock.Text += Environment.NewLine + lines[i];
            }
        }

        private async void GetRace_Click(object sender, RoutedEventArgs e)
        {
            Settings.IsEnabled = false;
            RaceType.IsEnabled = false;
            GetRace.IsEnabled = false;
  
            if (!DataFromATG)
            {
                ChooseRaceFirst.Visibility = Visibility.Visible;
                ComboBoxMeny.IsEnabled = false;
                // _ = MessageBox.Show("Du måste först välja travlopp i menyn. \nDärefter kan du använda detta kommandot ");
            }
            else
            {
                await Task.Run(() => Program.PythonWebScraping());
                WriteResultATG();
            }

            Settings.IsEnabled = true;
            RaceType.IsEnabled = true;
            GetRace.IsEnabled = true;
        }

        private void Close_Click(object sender, RoutedEventArgs e)
        {
            NotYetImplemnted.Visibility = Visibility.Collapsed;
            ChooseRaceFirst.Visibility = Visibility.Collapsed;
            stackPanel.Visibility= Visibility.Collapsed;
            About.Visibility = Visibility.Collapsed;
            ComboBoxMeny.IsEnabled = true;
        }  
    }
}