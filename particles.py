from pyglet.shapes import Star
import random


# Class for creating and animating particle effects
class Particles:
    def __init__(self, x, y):
        # Create a list of Rectangle shapes representing particles
        self.particles = []
        # Initial y-coordinate for the particles
        self.y = y + 50
        # Animation time parameter
        self.animation_time = -2
        # X and Y directions for each particle
        self.directions_x = []
        self.directions_y = []
        # Speed for each particle
        self.speeds = []

        # Create particles with random sizes, rotation angle, and colors
        for _ in range(3):
            outer_radius = random.randint(5, 15)
            inner_radius = outer_radius * 0.5
            color = self.random_color()
            rotation = random.uniform(0, 360)
            particle = Star(x, y, outer_radius, inner_radius, color=color, num_spikes=5, rotation=rotation)
            self.particles.append(particle)

            # Add corresponding random values for direction and speed
            self.directions_x.append(random.uniform(-10, 10))
            self.directions_y.append(random.uniform(5, 15))
            self.speeds.append(random.uniform(2, 5))

    # Method for drawing each particle on the screen
    def draw(self):
        for particle in self.particles:
            particle.draw()

    # Method for updating the animation time
    def update(self, elapsed_time):
        self.animation_time += elapsed_time * 20
        # List to store indices of particles to be removed
        particles_to_remove = []

        # Update the position of each particle based on animation time, direction, and speed
        for i, (particle, direction_x, direction_y, speed) in enumerate(
            zip(self.particles, self.directions_x, self.directions_y, self.speeds)
        ):
            # Random motion
            particle.y = self.y - self.animation_time ** 2 * speed + direction_y * elapsed_time * 10
            # Update the x-coordinate based on the particle's direction and the elapsed time
            particle.x += direction_x * elapsed_time * 10

            # Check if the particle is out of bounds
            if self.check_bounds(particle):
                particles_to_remove.append(i)

        # Remove particles that are out of bounds
        for index in reversed(particles_to_remove):
            del self.particles[index]
            del self.directions_x[index]
            del self.directions_y[index]
            del self.speeds[index]

    # Method to check if a particle is out of the visible bounds of the window
    def check_bounds(self, particle):
        return particle.y < -10 or particle.x < -10 or particle.x > 810

    # Generator function for generating a random RGBA color
    def random_color_generator(self):
        while True:
            yield (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
                255  # 255 for full opacity
            )

    # Method for getting the next random color from the generator
    def random_color(self):
        return next(self.random_color_generator())
