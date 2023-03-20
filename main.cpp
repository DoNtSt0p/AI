#include <SFML/Graphics.hpp>
#include <iostream>
#include <string>


#define vec2f sf::Vector2f


class App
{
public:
	sf::VideoMode mode;
	sf::RenderWindow window;
	vec2f pos;
	sf::Image image;
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
	App my_app;
	my_app.run();
	return 0;
}