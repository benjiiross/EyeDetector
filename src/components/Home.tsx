import ImageDropzone from "./ImageDropzone";
import EyeIcon from "./EyeIcon";

export default function Home() {
  return (
    <div
      className="text-center p-10 h-screen w-screen"
      style={{
        backgroundImage: "url('/background.jpg')",
        backgroundSize: "cover",
      }}
    >
      <div className="flex justify-center items-center space-x-2">
        <EyeIcon />
        <h2 className="text-2xl font-semibold">EyeDetector</h2>
      </div>

      <h1 className="text-4xl font-bold mt-10">Upload an eye image here</h1>
      <h2 className="text-xl font-semibold mt-2 text-gray-500">
        Supported formats are .jpg, .jpeg, .png
      </h2>

      <div className="mt-10">
        <ImageDropzone />
      </div>
    </div>
  );
}
