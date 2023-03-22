#include <SFML/Graphics.hpp>
#include <iostream>


int rnd(int a, int b)
{
	return std::rand() % (b - a + 1) + a;
}


struct Asset
{
	sf::Image image;
	int x, y, size;
	Asset(){};
	Asset(sf::Image I, int X, int Y, int S)
	{
		image = I;
		x = X; y = Y; size = S;
	}
};


Asset generate()
{	
	sf::RenderTexture surface;
	sf::RectangleShape rect;
	int BACKGROUND, FILL_COLOR, SIZE, X, Y; // random values

	BACKGROUND = rnd(159, 255);
	FILL_COLOR = rnd(0, 95);
	SIZE = rnd(10, 20) * 2;
	X = rnd(SIZE, 100 - SIZE);
	Y = rnd(SIZE, 100 - SIZE);
	rect.setSize(sf::Vector2f(SIZE, SIZE));
	rect.setPosition(sf::Vector2f(X, Y));
	rect.setOrigin(sf::Vector2f(SIZE / 2, SIZE / 2));
	rect.setFillColor(sf::Color(FILL_COLOR, FILL_COLOR, FILL_COLOR));
	
	surface.create(100, 100);
	surface.clear(sf::Color(BACKGROUND, BACKGROUND, BACKGROUND));
	surface.draw(rect);

	return Asset(surface.getTexture().copyToImage(), X, Y, SIZE);
}


class App
{
public:
	sf::VideoMode mode;
	sf::RenderWindow window;
	sf::Vector2f pos;
	Asset *source;
	int source_length;
	App();
	void
		draw_asset(),
		new_source(),
		run();
	~App();
};


App::App()
{
	mode = sf::VideoMode(500, 500);
	window.create(mode, "title");
	window.setFramerateLimit(120);
	source_length = 100;
	new_source();
}


void draw_asset()
{
	// later
}


void App::new_source()
{
	source = new Asset[source_length];
	for (int i = 0; i < source_length; i++)
		source[i] = generate();
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


App::~App()
{
	delete source;
}


int main()
{
	App my_app;
	my_app.run();
	return 0;
}