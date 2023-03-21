#include <SFML/Graphics.hpp>
#include <windows.h>
#include <iostream>
#include <fstream>
#include <string>


int rnd(int a, int b)
{
	return std::rand() % (b - a + 1) + a;
}


void generate()
{
	CreateDirectory("C:\\A\\storage", NULL);
	
	std::ofstream source_file("C:\\A\\storage\\source.txt");
	sf::RenderTexture surface;
	sf::RectangleShape rect;
	int BACKGROUND, FILL_COLOR, SIZE, X, Y; // random values

	surface.create(100, 100);
	for (int i = 0; i < 1000; i++)
	{
		BACKGROUND = rnd(159, 255);
		FILL_COLOR = rnd(0, 95);
		SIZE = rnd(10, 20) * 2;
		X = rnd(SIZE, 100 - SIZE);
		Y = rnd(SIZE, 100 - SIZE);
		rect.setSize(sf::Vector2f(SIZE, SIZE));
		rect.setPosition(sf::Vector2f(X, Y));
		rect.setOrigin(sf::Vector2f(SIZE / 2, SIZE / 2));
		rect.setFillColor(sf::Color(FILL_COLOR, FILL_COLOR, FILL_COLOR));
		surface.clear(sf::Color(BACKGROUND, BACKGROUND, BACKGROUND));
		surface.draw(rect);
		surface.getTexture().copyToImage().saveToFile("C:\\A\\storage\\" + std::to_string(i) + ".png");
		source_file << X << " " << Y << " " << SIZE;
		if (i != 999)
			source_file << "/n";
	}
	source_file.close();
}


class App
{
public:
	sf::VideoMode mode;
	sf::RenderWindow window;
	sf::Vector2f pos;
	sf::RenderTexture texture;
	App();
	void run();
};


App::App()
{
	mode = sf::VideoMode(500, 500);
	window.create(mode, "title");
	window.setFramerateLimit(120);
}


void App::run()
{
	while (window.isOpen())
	{
		window.clear();
		window.display();
		sf::Event e;
		while (window.pollEvent(e))
		{
			if (e.type == sf::Event::Closed)
				window.close();
		}
	}
}


int main()
{
	generate();
	App my_app;
	my_app.run();
	return 0;
}