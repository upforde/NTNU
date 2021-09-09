extern crate nalgebra_glm as glm;
use std::{ mem, ptr, os::raw::c_void };
use std::thread;
use std::sync::{Mutex, Arc, RwLock};

mod shader;
mod util;

use glutin::event::{Event, WindowEvent, DeviceEvent, KeyboardInput, ElementState::{Pressed, Released}, VirtualKeyCode::{self, *}};
use glutin::event_loop::ControlFlow;

const SCREEN_W: u32 = 800;
const SCREEN_H: u32 = 600;

// == // Helper functions to make interacting with OpenGL a little bit prettier. You *WILL* need these! // == //
// The names should be pretty self explanatory
fn byte_size_of_array<T>(val: &[T]) -> isize {
    std::mem::size_of_val(&val[..]) as isize
}

// Get the OpenGL-compatible pointer to an arbitrary array of numbers
fn pointer_to_array<T>(val: &[T]) -> *const c_void {
    &val[0] as *const T as *const c_void
}

// Get the size of the given type in bytes
fn size_of<T>() -> i32 {
    mem::size_of::<T>() as i32
}

// Get an offset in bytes for n units of type T
fn offset<T>(n: u32) -> *const c_void {
    (n * mem::size_of::<T>() as u32) as *const T as *const c_void
}

// Get a null pointer (equivalent to an offset of 0)
// ptr::null()


// == // Modify and complete the function below for the first task
unsafe fn set_up_vao(arr_vertices: &Vec<f32>, arr_indecies: &Vec<u32>) -> u32 { 
    // Creating and binding the VAO
    let mut array: u32 = 0;
    gl::GenVertexArrays(1, &mut array as *mut u32);
    gl::BindVertexArray(array);

    // Creating and binding the buffer
    let mut buffer: u32 = 0;
    gl::GenBuffers(1, &mut buffer as *mut u32);
    gl::BindBuffer(gl::ARRAY_BUFFER, buffer);

    // Filling the buffer
    gl::BufferData(gl::ARRAY_BUFFER, byte_size_of_array(&arr_vertices), pointer_to_array(&arr_vertices), gl::STATIC_DRAW);

    // Setting up the vertex attributes
    gl::VertexAttribPointer(0, 3, gl::FLOAT, gl::FALSE, 0, ptr::null());
    gl::EnableVertexAttribArray(0);

    // Setting up buffer for indecies
    let mut index: u32 = 0;
    gl::GenBuffers(1, &mut index as *mut u32);
    gl::BindBuffer(gl::ELEMENT_ARRAY_BUFFER, index);
    gl::BufferData(gl::ELEMENT_ARRAY_BUFFER, byte_size_of_array(&arr_indecies), pointer_to_array(&arr_indecies), gl::STATIC_DRAW);

    return array;
} 

fn main() {
    // Set up the necessary objects to deal with windows and event handling
    let el = glutin::event_loop::EventLoop::new();
    let wb = glutin::window::WindowBuilder::new()
        .with_title("Gloom-rs")
        .with_resizable(false)
        .with_inner_size(glutin::dpi::LogicalSize::new(SCREEN_W, SCREEN_H));
    let cb = glutin::ContextBuilder::new()
        .with_vsync(true);
    let windowed_context = cb.build_windowed(wb, &el).unwrap();
    // Uncomment these if you want to use the mouse for controls, but want it to be confined to the screen and/or invisible.
    // windowed_context.window().set_cursor_grab(true).expect("failed to grab cursor");
    // windowed_context.window().set_cursor_visible(false);

    // Set up a shared vector for keeping track of currently pressed keys
    let arc_pressed_keys = Arc::new(Mutex::new(Vec::<VirtualKeyCode>::with_capacity(10)));
    // Make a reference of this vector to send to the render thread
    let pressed_keys = Arc::clone(&arc_pressed_keys);

    // Set up shared tuple for tracking mouse movement between frames
    let arc_mouse_delta = Arc::new(Mutex::new((0f32, 0f32)));
    // Make a reference of this tuple to send to the render thread
    let mouse_delta = Arc::clone(&arc_mouse_delta);

    // Spawn a separate thread for rendering, so event handling doesn't block rendering
    let render_thread = thread::spawn(move || {
        // Acquire the OpenGL Context and load the function pointers. This has to be done inside of the rendering thread, because
        // an active OpenGL context cannot safely traverse a thread boundary
        let context = unsafe {
            let c = windowed_context.make_current().unwrap();
            gl::load_with(|symbol| c.get_proc_address(symbol) as *const _);
            c
        };

        // Set up openGL
        unsafe {
            gl::Enable(gl::DEPTH_TEST);
            gl::DepthFunc(gl::LESS);
            gl::Enable(gl::CULL_FACE);
            gl::Disable(gl::MULTISAMPLE);
            gl::Enable(gl::BLEND);
            gl::BlendFunc(gl::SRC_ALPHA, gl::ONE_MINUS_SRC_ALPHA);
            gl::Enable(gl::DEBUG_OUTPUT_SYNCHRONOUS);
            gl::DebugMessageCallback(Some(util::debug_callback), ptr::null());

            // Print some diagnostics
            println!("{}: {}", util::get_gl_string(gl::VENDOR), util::get_gl_string(gl::RENDERER));
            println!("OpenGL\t: {}", util::get_gl_string(gl::VERSION));
            println!("GLSL\t: {}", util::get_gl_string(gl::SHADING_LANGUAGE_VERSION));
        }

        // == // Set up your VAO here
        unsafe {
            // Task 1: 5 distinct triangles
            // let vertices: Vec<f32> = vec![
            //     0.75, -0.5, 0.0, 0.5, 0.0, 0.0, 0.25, -0.5, 0.0,    // Leftmost triangle bottom row
            //     0.5, 0.0, 0.0, 0.25, 0.5, 0.0, 0.0, 0.0, 0.0,       // Leftmost triangle middle row
            //     0.25, 0.5, 0.0, 0.0, 1.0, 0.0, -0.25, 0.5, 0.0,     // Upper row triangle
            //     0.25, -0.5, 0.0, 0.0, 0.0, 0.0, -0.25, -0.5, 0.0,   // Middle triangle bottom row
            //     0.0, 0.0, 0.0, -0.25, 0.5, 0.0, -0.5, 0.0, 0.0,     // Rightmost triangle middle row
            // ];

            // // // Indeces for connecting the vertices correctly together
            // let indeces: Vec<u32> = vec![
            //     1, 2, 0,
            //     4, 5, 3,
            //     7, 8, 6,
            //     10, 11, 9,
            //     13, 14, 12
            // ];

            //Task 2: a)
            // let vertices: Vec<f32> = vec![0.6, -0.8, -1.2, 0.0, 0.4, 0.0, -0.8, -0.2, 1.2];
            // let indeces: Vec<u32> = vec![1, 2, 0];

            // Task 2: b)
            let vertices: Vec<f32> = vec![-0.6, -0.6, 0.0, 0.6, -0.6, 0.0, 0.0, 0.6, 0.0];
            // Two sets of indices, one that's counter clockwise, and one that's clockwise
            let indices: Vec<u32> = vec![1, 2, 0];
            //let indices: Vec<u32> = vec![2, 1, 0];
            
            // Supplying the data to the VAO
            set_up_vao(&vertices, &indices);
        }

        unsafe {
            // TODO: fix the pathing, so that it's a relative path instead of an absolute one.
            // Setting up and activating the vertex shader
            /* let sh_vertex = */ shader::ShaderBuilder::new()
                .attach_file("/home/bigdikdinko/Documents/NTNU/CG/gloom-rs/shaders/simple.vert")
                .link()
                .activate();

            // Setting up and activating the fragment shader
            /* let sh_fragment = */ shader::ShaderBuilder::new()
                .attach_file("/home/bigdikdinko/Documents/NTNU/CG/gloom-rs/shaders/simple.frag")
                .link()
                .activate();
        }

        // Used to demonstrate keyboard handling -- feel free to remove
        let mut _arbitrary_number = 0.0;

        let first_frame_time = std::time::Instant::now();
        let mut last_frame_time = first_frame_time;
        // The main rendering loop
        loop {
            let now = std::time::Instant::now();
            let elapsed = now.duration_since(first_frame_time).as_secs_f32();
            let delta_time = now.duration_since(last_frame_time).as_secs_f32();
            last_frame_time = now;

            // Handle keyboard input
            if let Ok(keys) = pressed_keys.lock() {
                for key in keys.iter() {
                    match key {
                        VirtualKeyCode::A => {
                            _arbitrary_number += delta_time;
                        },
                        VirtualKeyCode::D => {
                            _arbitrary_number -= delta_time;
                        },


                        _ => { }
                    }
                }
            }
            // Handle mouse movement. delta contains the x and y movement of the mouse since last frame in pixels
            if let Ok(mut delta) = mouse_delta.lock() {



                *delta = (0.0, 0.0);
            }

            unsafe {
                gl::ClearColor(0.76862745, 0.71372549, 0.94901961, 1.0); // moon raker, full opacity
                gl::Clear(gl::COLOR_BUFFER_BIT | gl::DEPTH_BUFFER_BIT);

                // Issue the necessary commands to draw your scene here

                // Drawing the triangles
                gl::DrawElements(gl::TRIANGLES, 100, gl::UNSIGNED_INT, ptr::null());
            }

            context.swap_buffers().unwrap();
        }
    });

    // Keep track of the health of the rendering thread
    let render_thread_healthy = Arc::new(RwLock::new(true));
    let render_thread_watchdog = Arc::clone(&render_thread_healthy);
    thread::spawn(move || {
        if !render_thread.join().is_ok() {
            if let Ok(mut health) = render_thread_watchdog.write() {
                println!("Render thread panicked!");
                *health = false;
            }
        }
    });

    // Start the event loop -- This is where window events get handled
    el.run(move |event, _, control_flow| {
        *control_flow = ControlFlow::Wait;

        // Terminate program if render thread panics
        if let Ok(health) = render_thread_healthy.read() {
            if *health == false {
                *control_flow = ControlFlow::Exit;
            }
        }

        match event {
            Event::WindowEvent { event: WindowEvent::CloseRequested, .. } => {
                *control_flow = ControlFlow::Exit;
            },
            // Keep track of currently pressed keys to send to the rendering thread
            Event::WindowEvent { event: WindowEvent::KeyboardInput {
                input: KeyboardInput { state: key_state, virtual_keycode: Some(keycode), .. }, .. }, .. } => {

                if let Ok(mut keys) = arc_pressed_keys.lock() {
                    match key_state {
                        Released => {
                            if keys.contains(&keycode) {
                                let i = keys.iter().position(|&k| k == keycode).unwrap();
                                keys.remove(i);
                            }
                        },
                        Pressed => {
                            if !keys.contains(&keycode) {
                                keys.push(keycode);
                            }
                        }
                    }
                }

                // Handle escape separately
                match keycode {
                    Escape => {
                        *control_flow = ControlFlow::Exit;
                    },
                    Q => {
                        *control_flow = ControlFlow::Exit;
                    }
                    _ => { }
                }
            },
            Event::DeviceEvent { event: DeviceEvent::MouseMotion { delta }, .. } => {
                // Accumulate mouse movement
                if let Ok(mut position) = arc_mouse_delta.lock() {
                    *position = (position.0 + delta.0 as f32, position.1 + delta.1 as f32);
                }
            },
            _ => { }
        }
    });
}