    tailwind.config = {
      darkMode: ['class', '[data-theme="dark"]'],
      theme: {
        extend: {
          fontFamily: {
            sans: ['Plus Jakarta Sans', 'sans-serif'],
          },
          colors: {
            mateNavy: {
              DEFAULT: '#0B192C',
              50: '#f0f4f8',
              100: '#d9e2ec',
              800: '#0F2238',
              900: '#0B192C',
              950: '#060E1A'
            },
            mateGreen: {
              DEFAULT: '#00B87C',
              light: '#10B981',
              hover: '#009a67',
              bg: 'rgba(0, 184, 124, 0.12)'
            }
          }
        }
      }
    }
