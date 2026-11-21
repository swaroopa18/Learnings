/** @type {import('tailwindcss').Config} */
module.exports = {
  // NOTE: Update this to include the paths to all files that contain Nativewind classes.
  content: ["./src/app/**/*.{js,jsx,ts,tsx}", "./components/**/*.{js,jsx,ts,tsx}"],
  presets: [require("nativewind/preset")],
  theme: {
    extend: {
      colors: {
        primary: "#413DFF",
        error: {
          default: "#C70808",
        },
        black: {
          100: "#000000",
          80: "#000000CC",
          60: "#00000099",
          40: "#00000066",
          20: "#00000033",
          3: "#00000003",
        },
        grey: {
          700: "#4D4D4D",
          600: "#666666",
          500: "#808080",
          300: "#B3B3B3",
          100: "#E6E6E6",
          50: "#F5F5F5",
        },
        white: {
          100: "#FFFFFF",
          80: "#FFFFFFCC",
          70: "#FFFFFF70",
          60: "#FFFFFF99",
          40: "#FFFFFF66",
          20: "#FFFFFF33",
          54: "#FFFFFF1A",
        },
        red: {
          100: "#F83A3A",
          80: "#F83A3ACC",
          60: "#F83A3A99",
          40: "#F83A3A66",
          20: "#F83A3A33",
        },
        green: {
          100: "#22C55E",
          80: "#22C55ECC",
          60: "#22C55E99",
          40: "#22C55E66",
          20: "#22C55E33",
        },
        smoke: {
          100: "#EDEDED",
          80: "#EDEDEDCC",
          60: "#EDEDED99",
          40: "#EDEDED66",
          20: "#EDEDED33",
        },
        lightGrey: {
          100: "#F2F2F2",
          80: "#F2F2F2CC",
          60: "#F2F2F299",
          40: "#F2F2F266",
          20: "#F2F2F233",
        },
        blue: {
          100: "#518AE7",
          80: "#518AE7CC",
          60: "#518AE799",
          40: "#518AE766",
          20: "#518AE733",
        },
        pink: "#E61C5C",
        charcoal: {
          100: "#282828",
          80: "#282828CC",
          60: "#28282899",
          40: "#28282866",
          20: "#28282833",
        },
        success: {
          light: "#C7F4E9",
          100: "#07C799",
          80: "#07C799CC",
          60: "#07C79999",
          40: "#07C79966",
          20: "#07C79933",
        },
        navy: {
          100: "#0C1C3C",
        },
        orange: {
          100: "#CC6600",
        },
      },
      fontFamily: {
        TWKLausanne: ["TWKLausanne"],
      },
    },
  },
  plugins: [],
}